"""Add user accounts and link patient and doctor records.

Revision ID: 6054bc4c0814
Revises: c8734994d464
Create Date: 2026-10-06 16:00:52.831261
"""
from alembic import op
import sqlalchemy as sa


revision = '6054bc4c0814'
down_revision = 'c8734994d464'
branch_labels = None
depends_on = None


def _inspector():
    return sa.inspect(op.get_bind())


def _ensure_user_table():
    if 'users' not in _inspector().get_table_names():
        op.create_table(
            'users',
            sa.Column('user_id', sa.Integer(), autoincrement=True, nullable=False),
            sa.Column('email', sa.String(length=255), nullable=False),
            sa.Column('role', sa.Enum('doctor', 'patient', 'admin'), nullable=True),
            sa.Column('password_hash', sa.String(length=255), nullable=False),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint('user_id'),
            sa.UniqueConstraint('email', name='uq_users_email'),
        )


def _ensure_user_id_column(table):
    columns = {column['name'] for column in _inspector().get_columns(table)}
    if 'user_id' not in columns:
        op.add_column(table, sa.Column('user_id', sa.Integer(), nullable=True))


def _link_accounts(table, role):
    connection = op.get_bind()
    connection.execute(sa.text(f"""
        INSERT INTO users (email, role, password_hash, created_at)
        SELECT records.email, :role, records.password_hash, records.created_at
        FROM {table} AS records
        LEFT JOIN users AS accounts ON accounts.email = records.email
        WHERE accounts.user_id IS NULL
    """), {'role': role})
    connection.execute(sa.text(f"""
        UPDATE {table} AS records
        JOIN users AS accounts ON accounts.email = records.email
        SET records.user_id = accounts.user_id
        WHERE records.user_id IS NULL OR records.user_id <> accounts.user_id
    """))


def _ensure_user_constraints(table):
    inspector = _inspector()
    unique_user_id = any(
        constraint['column_names'] == ['user_id']
        for constraint in inspector.get_unique_constraints(table)
    ) or any(
        index['unique'] and index['column_names'] == ['user_id']
        for index in inspector.get_indexes(table)
    )
    if not unique_user_id:
        op.create_unique_constraint(f'uq_{table}_user_id', table, ['user_id'])

    inspector = _inspector()
    has_user_foreign_key = any(
        foreign_key['constrained_columns'] == ['user_id']
        and foreign_key['referred_table'] == 'users'
        and foreign_key['referred_columns'] == ['user_id']
        for foreign_key in inspector.get_foreign_keys(table)
    )
    if not has_user_foreign_key:
        op.create_foreign_key(
            f'fk_{table}_user_id_users',
            table,
            'users',
            ['user_id'],
            ['user_id'],
        )


def upgrade():
    _ensure_user_table()

    for table in ('doctors', 'patients'):
        _ensure_user_id_column(table)

    _link_accounts('doctors', 'doctor')
    _link_accounts('patients', 'patient')

    for table in ('doctors', 'patients'):
        op.alter_column(
            table,
            'user_id',
            existing_type=sa.Integer(),
            nullable=False,
        )
        _ensure_user_constraints(table)


def downgrade():
    for table in ('patients', 'doctors'):
        inspector = _inspector()
        for foreign_key in inspector.get_foreign_keys(table):
            if (
                foreign_key['constrained_columns'] == ['user_id']
                and foreign_key['referred_table'] == 'users'
            ):
                op.drop_constraint(foreign_key['name'], table, type_='foreignkey')

        inspector = _inspector()
        for constraint in inspector.get_unique_constraints(table):
            if constraint['column_names'] == ['user_id']:
                op.drop_constraint(constraint['name'], table, type_='unique')

        columns = {column['name'] for column in _inspector().get_columns(table)}
        if 'user_id' in columns:
            op.drop_column(table, 'user_id')
