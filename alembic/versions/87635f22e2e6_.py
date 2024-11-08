"""empty message

Revision ID: 87635f22e2e6
Revises: 49a88cdbb9e4
Create Date: 2024-09-15 10:57:22.509061

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '87635f22e2e6'
down_revision: Union[str, None] = '49a88cdbb9e4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('processoryprice', schema=None) as batch_op:
        batch_op.add_column(sa.Column('store', sa.String(), nullable=False))
        batch_op.alter_column('price',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.drop_constraint('_product_city_uc', type_='unique')
        batch_op.create_unique_constraint('_store_city_uc', ['store', 'city_id'])

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('processoryprice', schema=None) as batch_op:
        batch_op.drop_constraint('_store_city_uc', type_='unique')
        batch_op.create_unique_constraint('_product_city_uc', ['processory_id', 'city_id'])
        batch_op.alter_column('price',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.drop_column('store')

    # ### end Alembic commands ###
