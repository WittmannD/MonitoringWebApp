from marshmallow import fields, post_load, post_dump

from api.models.MonitorModel import MonitorModel
from api.models.Schemas.BaseSchema import ValidatedSchema
from api.models.Schemas.MonitorSchema import monitor_summary


class PaginationSchema(ValidatedSchema):
    page = fields.Integer(missing=1)
    per_page = fields.Integer(missing=10, load_only=True)
    order_by = fields.String(missing='created_at desc', load_only=True)

    items = fields.List(fields.Raw, dump_only=True)
    pages = fields.Integer(dump_only=True)
    total = fields.Integer(dump_only=True)

    @post_load()
    def process_input_data(self, data, **kwargs):
        try:
            field, direction = data.get('order_by').split(' ')
            assert field in MonitorModel.__dict__
            assert direction in MonitorModel.__dict__[field].__dict__

        except (ValueError, AssertionError):
            data['order_by'] = 'created_at desc'

        return data

