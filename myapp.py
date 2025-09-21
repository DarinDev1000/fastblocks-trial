from acb.adapters import import_adapter
from acb.depends import depends

Templates = import_adapter("templates")


@depends.inject
async def homepage(request, templates: Templates = depends()):
    # Render a full template
    return await templates.app.render_template(
        request,
        "index.html",  # Template file path relative to templates directory
        context={"title": "FastBlocks Demo", "user": {"name": "John"}},
    )