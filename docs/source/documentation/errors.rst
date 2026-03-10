########
 Errors
########

|  All of the custom errors that are used within WarMAC.

************
 Base Error
************

.. autoexception:: errors.WarMACBaseError
   :show-inheritance:
   :exclude-members: __init__

Generic Errors
==============

.. autoexception:: errors.CommandError
   :show-inheritance:
   :exclude-members: __init__


.. autoexception:: errors.NoListingsFoundError
   :show-inheritance:
   :exclude-members: __init__

HTTP Errors
===========

.. autoexception:: errors.WarMACHTTPError
   :show-inheritance:
   :exclude-members: __init__

.. autoexception:: errors.UnauthorizedAccessError
   :show-inheritance:
   :exclude-members: __init__

.. autoexception:: errors.ForbiddenRequestError
   :show-inheritance:
   :exclude-members: __init__

.. autoexception:: errors.MalformedURLError
   :show-inheritance:
   :exclude-members: __init__

.. autoexception:: errors.MethodNotAllowedError
   :show-inheritance:
   :exclude-members: __init__

.. autoexception:: errors.InternalServerError
   :show-inheritance:
   :exclude-members: __init__

.. autoexception:: errors.RateLimitError
   :show-inheritance:
   :exclude-members: __init__

.. autoexception:: errors.UnknownError
   :show-inheritance:
   :exclude-members: __init__
