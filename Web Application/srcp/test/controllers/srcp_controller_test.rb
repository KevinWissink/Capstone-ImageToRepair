require "test_helper"

class SrcpControllerTest < ActionDispatch::IntegrationTest
  test "should get index" do
    get srcp_index_url
    assert_response :success
  end

  test "should get upload_images" do
    get srcp_upload_images_url
    assert_response :success
  end

  test "should get about_us" do
    get srcp_about_us_url
    assert_response :success
  end

  test "should get contact" do
    get srcp_contact_url
    assert_response :success
  end
end
