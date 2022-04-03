from multidict import MultiDict


def get_headers_for_zip_file(output_filename: str) -> MultiDict[str]:
    content_dispos = "attachment;filename={0}".format(
            output_filename + ".zip"
        )
    return MultiDict({
        "Content-Type": "application/zip",
        "Content-Disposition": content_dispos,
        })
