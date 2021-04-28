def test_post(delivery_service, couponed_course):
    assert delivery_service.post(couponed_course) is not None
