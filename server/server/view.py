import sanic


class BaseView(sanic.views.HTTPMethodView):
    # pylint: disable=too-few-public-methods

    @staticmethod
    def get_field(request, field, default=None):
        """Helper method for getting a specified field from the JSON fields in
        a request object.

        Args:
            request: A :sanic:`request_data` object.
            field (str): Field to be looked up.
            default (optional): Default value to return if the field is
                missing.

        Returns:
            The value of the specified field contained in the request object,
            if present. If the field is missing but a default was provided,
            returns the default object.

        Raises:
            InvalidUsage(400): The field was not provided and no default was
                set.
        """
        try:
            return request.json[field]
        except KeyError:
            if default is not None:
                return default

            raise sanic.exceptions.InvalidUsage(
                'missing {} field'.format(field))
