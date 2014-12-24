from django.test import TestCase, RequestFactory
from django.http import HttpResponse
from django.views.generic.base import View
from django.core.exceptions import ImproperlyConfigured

from thoughts.decorators import view_decorator, ajax_only


class ViewDecoratorTestCase(TestCase):
    TEST_DECORATOR_RESPONSE = 'OK'

    def setUp(self):
        @view_decorator
        def test_decorator(f, request, *args, **kwargs):
            return self.TEST_DECORATOR_RESPONSE
        self.test_decorator = test_decorator
        self.request_factory = RequestFactory()

    def test_fails_on_unknown_classes(self):
        with self.assertRaises(ImproperlyConfigured):
            @self.test_decorator
            class SomeUnknownThing():
                pass

    def test_works_on_class_based_views(self):
        @self.test_decorator
        class TestView(View):
            pass
        test_view = TestView.as_view()
        request = self.request_factory.get('/some/place/')
        response = test_view(request)
        self.assertEqual(response, self.TEST_DECORATOR_RESPONSE)

    def test_works_on_function_views(self):
        @self.test_decorator
        def test_view():
            pass
        request = self.request_factory.get('/some/place/')
        response = test_view(request)
        self.assertEqual(response, self.TEST_DECORATOR_RESPONSE)


class IsAJAXTestCase(TestCase):
    OK_RESPONSE_CONTENT = b'OK'

    def setUp(self):
        @ajax_only
        def test_view(request):
            return HttpResponse(self.OK_RESPONSE_CONTENT)
        self.test_view = test_view
        self.request_factory = RequestFactory()

    def test_returns_bad_response_on_non_ajax_requests(self):
        request = self.request_factory.get('/some/place/')
        response = self.test_view(request)
        self.assertEqual(response.status_code, 400)

    def test_returns_proper_response_on_ajax_requests(self):
        request = self.request_factory.get(
            '/some/place',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response = self.test_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, self.OK_RESPONSE_CONTENT)
