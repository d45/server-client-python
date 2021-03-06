import xml.etree.ElementTree as ET
from .exceptions import UnpopulatedPropertyError
from .. import NAMESPACE


class ViewItem(object):
    def __init__(self):
        self._content_url = None
        self._id = None
        self._image = None
        self._initial_tags = set()
        self._name = None
        self._owner_id = None
        self._preview_image = None
        self._total_views = None
        self._workbook_id = None
        self.tags = set()

    @property
    def content_url(self):
        return self._content_url

    @property
    def id(self):
        return self._id

    @property
    def image(self):
        return self._image

    @property
    def name(self):
        return self._name

    @property
    def owner_id(self):
        return self._owner_id

    @property
    def preview_image(self):
        if self._preview_image is None:
            error = "View item must be populated with its preview image first."
            raise UnpopulatedPropertyError(error)
        return self._preview_image

    @property
    def total_views(self):
        return self._total_views

    @property
    def workbook_id(self):
        return self._workbook_id

    @classmethod
    def from_response(cls, resp, workbook_id=''):
        return cls.from_xml_element(ET.fromstring(resp), workbook_id)

    @classmethod
    def from_xml_element(cls, parsed_response, workbook_id=''):
        all_view_items = list()
        all_view_xml = parsed_response.findall('.//t:view', namespaces=NAMESPACE)
        for view_xml in all_view_xml:
            view_item = cls()
            usage_elem = view_xml.find('.//t:usage', namespaces=NAMESPACE)
            workbook_elem = view_xml.find('.//t:workbook', namespaces=NAMESPACE)
            owner_elem = view_xml.find('.//t:owner', namespaces=NAMESPACE)
            view_item._id = view_xml.get('id', None)
            view_item._name = view_xml.get('name', None)
            view_item._content_url = view_xml.get('contentUrl', None)
            if usage_elem is not None:
                total_view = usage_elem.get('totalViewCount', None)
                if total_view:
                    view_item._total_views = int(total_view)

            if owner_elem is not None:
                view_item._owner_id = owner_elem.get('id', None)
            all_view_items.append(view_item)

            if workbook_id:
                view_item._workbook_id = workbook_id
            elif workbook_elem is not None:
                view_item._workbook_id = workbook_elem.get('id', None)
        return all_view_items
