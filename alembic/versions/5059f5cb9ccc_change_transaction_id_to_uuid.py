"""Change transaction_id from Integer to UUID"""
revision = '5059f5cb9ccc'
down_revision = '68b55600e39b'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa



def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto";')
    op.drop_constraint('transactions_pkey', 'transactions', type_='primary')
    op.execute('ALTER TABLE transactions ALTER COLUMN transaction_id DROP DEFAULT;')
    op.execute('ALTER TABLE transactions ALTER COLUMN transaction_id TYPE uuid USING gen_random_uuid();')
    op.execute('ALTER TABLE transactions ALTER COLUMN transaction_id SET DEFAULT gen_random_uuid();')
    op.create_primary_key('transactions_pkey', 'transactions', ['transaction_id'])

def downgrade() -> None:
    op.drop_constraint('transactions_pkey', 'transactions', type_='primary')
    op.execute('ALTER TABLE transactions ALTER COLUMN transaction_id DROP DEFAULT;')
    op.execute('ALTER TABLE transactions ALTER COLUMN transaction_id TYPE integer USING NULL;')
    op.execute("ALTER TABLE transactions ALTER COLUMN transaction_id SET DEFAULT nextval('transactions_transaction_id_seq');")
    op.create_primary_key('transactions_pkey', 'transactions', ['transaction_id'])
