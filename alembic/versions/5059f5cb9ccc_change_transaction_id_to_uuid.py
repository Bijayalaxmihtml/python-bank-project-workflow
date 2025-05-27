from alembic import op
import sqlalchemy as sa

def upgrade() -> None:
    # Ensure pgcrypto extension is available
    op.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto";')

    # Drop the existing primary key constraint on transaction_id
    op.drop_constraint('transactions_pkey', 'transactions', type_='primary')

    # Alter the column type from integer to UUID, generating new UUIDs for existing rows
    op.execute('ALTER TABLE transactions ALTER COLUMN transaction_id DROP DEFAULT;')
    op.execute('ALTER TABLE transactions ALTER COLUMN transaction_id TYPE uuid USING gen_random_uuid();')
    op.execute('ALTER TABLE transactions ALTER COLUMN transaction_id SET DEFAULT gen_random_uuid();')

    # Recreate the primary key constraint on the new UUID column
    op.create_primary_key('transactions_pkey', 'transactions', ['transaction_id'])


def downgrade() -> None:
    # Drop primary key constraint
    op.drop_constraint('transactions_pkey', 'transactions', type_='primary')

    # Alter the column back to integer, trying to cast UUID to integer (might fail if UUIDs don’t fit integer)
    # Alternatively, you could set it to a serial integer, but here we try simple cast
    op.execute('ALTER TABLE transactions ALTER COLUMN transaction_id DROP DEFAULT;')
    op.execute("ALTER TABLE transactions ALTER COLUMN transaction_id TYPE integer USING NULL;")
    # Set default sequence again
    op.execute("ALTER TABLE transactions ALTER COLUMN transaction_id SET DEFAULT nextval('transactions_transaction_id_seq');")

    # Recreate primary key constraint on integer column
    op.create_primary_key('transactions_pkey', 'transactions', ['transaction_id'])
