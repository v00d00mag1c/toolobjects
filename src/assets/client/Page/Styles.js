function _get_style(style) {
    return fetch(style).then((response) => {
        return response.text()
    })
}

export const default_page_styles = async function () {
    return await _get_style('/static/client/Styles/Common.css')
}

export default default_page_styles
