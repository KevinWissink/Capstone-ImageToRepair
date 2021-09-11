class SrcpController < ApplicationController
  def index
  end

  def contact
  end

  def new
    @user = User.new
  end

  def upload_images
    @user = User.new(params[:avatar])
  end

  def about_us
  end
end
