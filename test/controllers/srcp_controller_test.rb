require "test_helper"

class SrcpControllerTest < ActionDispatch::IntegrationTest
  test "should get index" do
    get srcp_index_url
    assert_response :success
  end
end
