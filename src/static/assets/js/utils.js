
export const renderForm = (container) => {
    const clone = $(FORMS[container]).html()
    $(`#${container}`).append(clone)
}

export const getAllInputs = (element) => {
    const inputs = []

    const inputsArr = element.getElementsByTagName("input")
    const selectsArr = element.getElementsByTagName("select")

    for (let i = 0; i < inputsArr.length; i++) {
        inputs.push(inputsArr[i]);
    }

    for (let j = 0; j < selectsArr.length; j++) {
        inputs.push(selectsArr[j]);
    }
    return inputs
}

export const extractData = (formSelector, postProcess) => {
    let cleanData;
    const data = []
    const forms = $(formSelector)
    forms.toArray().forEach((element) => {
        const item = {}
        const inputs = getAllInputs(element)
        inputs.reduce((accum, curr) => {
            item[$(curr).attr('name')] = $(curr).val()
            if ($(curr).attr('type') == 'checkbox') {
                item[$(curr).attr('name')] = curr.checked
            }
            return item
        }, item)
        data.push(item)
    })
    if (postProcess) {
        cleanData = postProcess(data)
    } else {
        cleanData = data
    }
    return cleanData
}

export const FORMS = {
    "names-container": "#name-form",
    "sanctions-container": "#sanction-form",
    "adresses-container": "#adress-form",
    "identities-container": "#identity-form",
    "person-roles-container": "#person-role-form"
}