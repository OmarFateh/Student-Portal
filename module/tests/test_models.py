from django.urls import reverse


def test_module_str(new_module):
    """
    Test module obj str method.
    """
    assert new_module.__str__() == 'introduction | physics'

def test_add_page_absolute_url(client, new_user, new_module):
    """
    Test add page reverse url response status.
    """
    url = reverse("page:add-page", kwargs={"course_slug": new_module.course.slug, "module_id": new_module.id})
    response = client.get(url)
    assert response.wsgi_request.user.is_authenticated is True
    assert response.status_code == 200
    assert new_module.get_add_page_absolute_url() == url

def test_add_quiz_absolute_url(client, new_user, new_module):
    """
    Test add quiz reverse url response status.
    """
    url = reverse("quiz:add-quiz", kwargs={"course_slug": new_module.course.slug, "module_id": new_module.id})
    response = client.get(url)
    assert response.status_code == 200
    assert new_module.get_add_quiz_absolute_url() == url

def test_add_assignment_absolute_url(client, new_user, new_module):
    """
    Test add assignment reverse url response status.
    """
    url = reverse("assignment:add-assignment", kwargs={"course_slug": new_module.course.slug, "module_id": new_module.id})
    response = client.get(url)
    assert response.status_code == 200
    assert new_module.get_add_assignment_absolute_url() == url