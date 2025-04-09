from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrAdminForDelete(BasePermission):
    """
    - اجازه PUT/PATCH فقط برای صاحب نظر
    - اجازه DELETE فقط برای ادمین
    - اجازه GET برای همه
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if request.method in ['PUT', 'PATCH']:
            return obj.user == request.user  # فقط مالک

        if request.method == 'DELETE':
            return request.user.is_staff  # فقط ادمین

        return False
