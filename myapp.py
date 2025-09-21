from starlette.routing import Route
from acb.adapters import import_adapter
from acb.depends import depends

# Import adapters - these are pluggable components that FastBlocks uses
# The Templates adapter handles rendering Jinja2 templates
# The App adapter provides the FastBlocks application instance

Templates = import_adapter("templates")  # Get the configured template adapter
App = import_adapter("app")  # Get the configured app adapter

# Templates = None
# App = None

# async def startup():
#     global Templates, App
#     adapters = await gather_imports(["templates", "app"])
#     Templates = adapters["templates"]
#     App = adapters["app"]
# startup()


# Define a route handler for the homepage
# The @depends.inject decorator automatically provides dependencies
@depends.inject
async def homepage(request, templates: Templates = depends()):
    # Render a template and return the response
    # This is similar to Flask's render_template but async
    return await templates.app.render_template(
        request, "index.html", context={"title": "FastBlocks Demo"}
    )


# Define your application routes
routes = [
    Route("/", endpoint=homepage)  # Map the root URL to the homepage function
]


# Create a counter endpoint that demonstrates HTMX functionality
# This will handle both GET and POST requests
@depends.inject
async def counter_block(request, templates: Templates = depends()):
    # Get the current count from the session or default to 0
    count = request.session.get("count", 0)

    # If this is a POST request, increment the counter
    if request.method == "POST":
        count += 1
        request.session["count"] = count

    # Render just the counter block with the current count
    return await templates.app.render_template(
        request, "blocks/counter.html", context={"count": count}
    )


# Add the counter route
routes.append(Route("/block/counter", endpoint=counter_block, methods=["GET", "POST"]))

# Get the FastBlocks application instance
# This is pre-configured based on your settings
app = depends.get(App)
