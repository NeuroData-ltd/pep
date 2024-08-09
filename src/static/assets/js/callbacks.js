import { FORMS, renderForm, getAllInputs, extractData } from "./utils.js"

$("#uploader").change(async (e) => {
    try {
        const formData = new FormData()
        formData.append("file", e.target.files[0])
        const res = await fetch("/upload-image", {
            method: "POST",
            body: formData,
            headers: {
                "contentType": "multipart/form-data",
                "Accept": "*/*"
            }
        })
        const data = await res.json()
        $("input[name=image_url]").val(data?.url)
        $("#photo-box").removeClass("d-none")
        console.log($("#photo-box > img")[0]);
        $("#photo-box > img").attr("src", data?.url)
    } catch (error) {
        alert("Uploading Image Error");
    }
})

$(".btn-add").on('click', (e) => {
    e.preventDefault()
    let p = e.target.parentElement.parentElement
    let container = p.getAttribute("id")
    renderForm(container)
    $(".btn-delete").on('click', (e) => {
        e.preventDefault();
        let p = $(e.target.parentElement.parentElement.parentElement.parentElement);
        console.log(p);
        p.remove()
    })
})

$("#primary-form").on('submit', async (e) => {
    e.preventDefault()

    const fn = (arr) => (arr.map((item) => {
        item.keyword = (typeof item.keyword !== 'undefined' && item.keyword.length > 0) ? JSON.parse(item.keyword)?.map((obj) => (obj?.value)) : [];
        item.source_name = (typeof item.source_name !== 'undefined' && item.source_name.length > 0) ? JSON.parse(item.source_name).map((obj) => (obj?.value)) : [];
        item.category = (typeof item.category !== 'undefined' && item.category.length > 0) ? JSON.parse(item.category).map((obj) => (obj?.value)) : [];
        item.country_code = (typeof item.country_code !== 'undefined' && item.country_code.length > 0) ? JSON.parse(item.country_code).map((obj) => (obj?.code)) : [];
        return arr
    }))

    const data = {
        "person_info": extractData("#main-form", fn)[0],
        "identities": extractData(".identity-form"),
        "names": extractData(".name-form"),
        "sanctions": extractData(".sanction-form"),
        "adresses": extractData(".adress-form"),
        "person_roles": extractData(".person-role-form")
    }

    if (data.names.length === 0) {
        alert("cannot insert PEP without name")
    } else {
        const res = await fetch("/add-xg4MOkc88x", {
            method: "POST",
            body: JSON.stringify(data),
            headers: {
                "Content-Type": "application/json",
            }
        })
        const payload = await res.json()
        $("#msg-container").text(payload["message"])
    }
})