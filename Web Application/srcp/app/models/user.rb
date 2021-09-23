class User < ApplicationRecord
  include Clearance::User
  has_many_attached :avatar
end
