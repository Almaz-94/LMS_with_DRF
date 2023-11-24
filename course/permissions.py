from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.creator


class IsModerator(BasePermission):

    def has_permission(self, request, view):
        return request.user.has_perms(perm_list=['course.change_course', 'course.change_lesson'])
