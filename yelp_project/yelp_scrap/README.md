# API Documentation

## GET APIS

``
GET-/yelp/restaurants/listings
``
This is a GET api that does the job of extracting list of restaurants from yelp website.It follows the next pages and
extracts restaurant data that includes restaurant name, restaurant image link,restaurant image,ratings, categories,
features and highlights.

``
GET-/yelp/restaurants/details
``
This is a GET api that does the job of extracting restaurant details from yelp website.It initially gets restaurant
links from the database and follows them. From the restaurant detail page extracts more restaurant data that includes
location,contact number, business website, more categories, more features, more highlights and menu items.

``
GET-/yelp/homeservices/listings
``
This is a GET api that does the job of extracting list of home services from yelp website.It follows the next pages and
extracts home service data that includes business name, business image link,business image,ratings, categories,
features and highlights.

``
GET-/yelp/homeservices/details
``
This is a GET api that does the job of extracting home services details from yelp website.It initially gets home service
links from the database and follows them. From the business detail page of the home service extracts more data that
includes
location,contact number, business website, more categories, more features, more highlights.

``
GET-/yelp/autoservices/listings
``
This is a GET api that does the job of extracting list of auto services from yelp website.It follows the next pages and
extracts auto service data that includes business name, business image link,business image,ratings, categories,
features and highlights.

``
GET-/yelp/autoservices/details
``
This is a GET api that does the job of extracting auto services details from yelp website.It initially gets auto service
links from the database and follows them. From the business detail page of the auto service extracts more data that
includes
location,contact number, business website, more categories, more features, more highlights.

``
GET-/yelp/others/listings
``
This is a GET api that does the job of extracting list of other services from yelp website.It follows the next pages and
extracts other service data that includes business name, business image link,business image,ratings, categories,
features and highlights.

``
GET-/yelp/others/details
``
This is a GET api that does the job of extracting other services details from yelp website.It initially gets other
service
links from the database and follows them. From the business detail page of the other service extracts more data that
includes
location,contact number, business website, more categories, more features, more highlights.

``
GET-/yelp/categories
``
This is a GET api that does the job of extracting categories from yelp website.It goes to yelp.com fetches categories by
hovering business dropdowns, and further following those business type buttons URLS

``
GET-/yelp/recent-activities
``
This is a GET api that does the job of extracting categories from yelp website.It goes to yelp.com fetches categories by
hovering business dropdowns, and further following those business type buttons URLS

``
GET-/yelp/events
``
This is a GET api that does the job of extracting events from yelp website.It goes to https://www.yelp.com/events in
that page browses to the all popular events and from that page extracts data like event title,date, link,location,image
link and type of image and follows the next page urls and extract data from that as well.

``
GET-/yelp/articles
``
This is a GET api that does the job of extracting blogs/articles from yelp website.It goes to https://blog.yelp.com/
fetches articles by
following category wise blog pages, and extracts blog details like blog title, blog tag, image if any, date and link

``
GET-/yelp/emails
``
This is a GET api that does the job of extracting emails from all pages of yelp website.
