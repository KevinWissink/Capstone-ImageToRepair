Rails.application.routes.draw do
  # get 'sessions/new'
  # get 'sessions/create'
  # get 'sessions/destroy'
  # resources :users

  # default route
  root 'srcp#index'

  get 'srcp/index'
  get 'srcp/upload_images'
  get 'srcp/about_us'
  get 'srcp/contact'

  # default route
  # get ':controller(/:action(/:id))'

  # For details on the DSL available within this file, see https://guides.rubyonrails.org/routing.html
end
