class HandoverHandler {
    constructor() {
        window.addEventListener('DOMContentLoaded', () => {
           this.initializeEventListeners()
        });

        // Disable Warning message in console.
        document.addEventListener("DOMContentLoaded", function () {
            document.addEventListener('hide.bs.modal', function (event) {
                if (document.activeElement) {
                    document.activeElement.blur();
                }
            });
        });

    }

    // Create Initializers for when page loads.
    initializeEventListeners() {
        this.setDate()
        this.initializeTooltips()
        this.setupTableFormSave()
    };

    // Add row dynamically.
    addRow(tableId) {
        const tbody = document.getElementById(tableId);
        const newRow = document.createElement('tr');
        newRow.innerHTML = `
            <td><input type="text" class="form-control handover-form-control" required></td>
            <td><textarea class="form-control handover-form-control" rows="2" required></textarea></td>
            <td>
                <button type="button" class="btn btn-danger btn-sm handover-btn" onclick="handover.removeRow(this)">
                    <i class="bi bi-trash"></i> Remove
                </button>
            </td>
        `;
        tbody.append(newRow);

    }

    // Add row dynamically
    addAlternateRow(tableId) {
        const tbody = document.getElementById(tableId);
        const newRow = document.createElement('tr');
        newRow.innerHTML = `
            <td><input type="text" class="form-control handover-form-control" required></td>
            <td><input type="text" class="form-control handover-form-control" required></td>
            <td><textarea class="form-control handover-form-control" rows="2" required></textarea></td>
            <td>
                <button type="button" class="btn btn-danger btn-sm handover-btn" onclick="handover.removeRow(this)">
                    <i class="bi bi-trash"></i> Remove
                </button>
            </td>
        `;
        tbody.appendChild(newRow);
    }

    // Loops through each table, to allow saving multiple tables at once.
    setupTableFormSave() {
        const form = document.getElementById("handover-form");
        if (!form) {
            return;
        }

        form.addEventListener("submit", (event) => {
            const tableIDs = ["non-standard-flights", "naifr-flights", "aog-flights", "com-flights"];
            tableIDs.forEach(tableID => this.table_form_save(tableID, form));

            form.submit();
        });
    }

    // Save the table passed in.
    table_form_save(tbodyID, form) {
        let tableData = [];
        let tbody = document.getElementById(tbodyID);

        if (!tbody) {
            return;
        }

        tbody.querySelectorAll("tr").forEach(row => {
            let rowData = [];

            row.querySelectorAll("td").forEach(cell => {
                let field = cell.querySelector("input, select, textarea");
                if (cell.querySelector("button")) return; // Skip adding the button column.

                // Push the data to the array.
                rowData.push(field ? field.value.trim() : cell.innerText.trim());
            });

            if (rowData.some(value => value !== "")) {
                tableData.push(rowData);
            }
        });

        // Create empty element to add all the table data for posting data.
        let hiddenInput = document.querySelector(`[name="${tbodyID}_json"]`);
        if (!hiddenInput) {
            hiddenInput = document.createElement("input");
            hiddenInput.type = "hidden";
            let hidden_name = tbodyID.replaceAll("-", "_")
            hiddenInput.name = `${hidden_name}_json`;
            form.appendChild(hiddenInput);
        }

        hiddenInput.value = JSON.stringify(tableData);
    }

    // Remove row dynamically.
    removeRow(button) {
        const row = button.closest('tr')
        row.style.opacity = '0';
        row.style.transform = 'translateX(20px)';
        setTimeout(() => {
            row.remove();
        }, 300);
    }

    // Set date. Either today or yesterday. Today = Main Form / Yesterday - Pop up dialog box.
    setDate() {
        const todayDate = document.getElementById('todayDate')
        const yesterdayDate = document.getElementById('previousDate')
        const today = new Date();

        todayDate.value = today.toISOString().split('T')[0]
        todayDate.setAttribute("max", todayDate.value)

        if (yesterdayDate) {
            let yesterday = new Date(today);
            yesterday.setDate(today.getDate() - 1);
            yesterdayDate.value = yesterday.toISOString().split('T')[0];
            yesterdayDate.setAttribute("max", yesterdayDate.value);
        }
    }

    // Load Previous data - Comes from pop up dialog.
    loadPreviousData() {
        let selectedDate = document.getElementById("previousDate").value;
        let selectedShift = document.getElementById("previousShift").value;

        if (!selectedDate || !selectedShift) {
            alert("Please select both a date and shift.");
            return;
        }

        // Fetch the data from Django
        fetch(`load-previous-data/?shift_date=${selectedDate}&shift_type=${selectedShift}`)
            .then(response => response.json())
            .then(data => {
                if (!data.error && data.data.length > 0) {
                    // Close Modal
                    $('#loadDataModal').modal('hide');
                    $('.modal-backdrop').remove();
                    $(document).on('hidden.bs.modal', '#loadDataModal', function () {
                        $('body').css('overflow', 'auto');
                    });

                    // Get Data
                    const handoverData = data.data[0];
                    const shiftDropdown = document.getElementById('shift');

                    // Select the Shift from dropdown
                    for (let option of shiftDropdown.options) {
                        if (option.text === handoverData.shift) {
                            option.selected = true;
                            break;
                        }
                    }

                    // Set AOG table.
                    const tableBody = document.getElementById('aog-flights');


                    const aog_element = document.getElementById('importAOG')
                    if (aog_element.checked) {
                        if (handoverData.aog.length > 0) {
                            tableBody.innerHTML = '';
                        }

                        for (const aog_item of handoverData.aog) {
                            const newRow = document.createElement("tr");

                            newRow.innerHTML = `
                            <td><input type="text" class="form-control handover-form-control" required value="${aog_item.tail}"></td>
                            <td><input type="text" class="form-control handover-form-control" required value="${aog_item.fob}"></td>
                                                    <td><textarea class="form-control handover-form-control" rows="2" required>${aog_item.issue}</textarea></td>
                            <td>
                                <button type="button" class="btn btn-danger btn-sm handover-btn" onclick="handover.removeRow(this)">
                                    <i class="bi bi-trash"></i> Remove
                                </button>
                            </td>
                            `
                            tableBody.appendChild(newRow);
                        }
                    }


                    // Loop through elements to only load selected data.
                    const elements = [
                        { checkboxId: 'importMELS', elementId: 'mels', dataKey: 'mels' },
                        { checkboxId: 'importProcedural', elementId: 'procedural_changes', dataKey: 'procedural_changes' },
                        { checkboxId: 'importNavblue', elementId: 'navblue_tickets', dataKey: 'navblue_tickets' },
                        { checkboxId: 'importOperationalNotams', elementId: 'notams', dataKey: 'operational_notams' }
                    ];

                    elements.forEach(item => {
                        const checkbox = document.getElementById(item.checkboxId);
                        const element = document.getElementById(item.elementId);

                        if (checkbox.checked) {
                            element.value = handoverData[item.dataKey];

                        }else {
                            if (!element.hasAttribute('data-user-input')) {
                                element.value = '';
                            }
                        }
                    })


                } else {
                        const errorMessage = document.createElement('p');
                        errorMessage.innerText = "No Handover Found for that date and shift type"
                        errorMessage.classList.add('alert', 'alert-danger', 'mt-4');
                        errorMessage.style.marginBottom = "-0.5rem";

                        const modalBody = document.querySelector('.modal-body.handover-modal-body');
                        modalBody.appendChild(errorMessage)
                    }
            })
    }

    initializeTooltips() {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
        tooltipTriggerList.forEach(function (tooltipTriggerEl) {
          new bootstrap.Tooltip(tooltipTriggerEl, {
            html: true   // tell Bootstrap we allow HTML!
          })
        })
    }
}

class HandoverViewHandler {
    constructor() {
        window.addEventListener('DOMContentLoaded', () => {
           this.initializeEventListeners()
        });
    }

    initializeEventListeners() {
        this.setDate()
        this.initializeTooltips()
    };

    setDate() {
        const todayDate = document.getElementById('todayDate')
        const today = new Date();

        todayDate.value = today.toISOString().split('T')[0]
        todayDate.setAttribute("max", todayDate.value)
    }

    initializeTooltips() {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
        tooltipTriggerList.forEach(function (tooltipTriggerEl) {
          new bootstrap.Tooltip(tooltipTriggerEl, {
            html: true   // tell Bootstrap we allow HTML!
          })
        })
    }

    load_previous_data() {
        let selectedDate = document.getElementById("todayDate").value;
        let selectedShift = document.getElementById("shift_type").value;
        const handoverCard = document.getElementById('handoverDataCard');
        const handoverSelector = document.getElementById('handover-data-selector');
        const existingErrorMessage = handoverSelector.querySelector('.alert-danger');
        if (existingErrorMessage) {
            existingErrorMessage.remove()
        }

        if (!selectedDate || !selectedShift) {
            alert("Please select both a date and shift.");
            return;
        }

        // CHECK CHECKBOXES

        const elements = [
            {elementId: 'dispatcher_name', dataKey: 'dispatcher_name'},
            {elementId: 'chief_duty_name', dataKey: 'chief_duty_name'},
            {elementId: 'shift_highlights', dataKey: 'shift_highlights'},
            {elementId: 'critical_fuel', dataKey: 'fuel_payload_critical'},
            {elementId: 'weather_issues', dataKey: 'weather_issues'},
            {elementId: 'operational_notams', dataKey: 'operational_notams'},
            {elementId: 'enroute_weather', dataKey: 'enroute_weather'},
            {elementId: 'mels', dataKey: 'mels'},
            {elementId: 'cdd_network_summary', dataKey: 'cdd_network_summary'},
            {elementId: 'misc', dataKey: 'misc'},
            {elementId: 'it_issues', dataKey: 'it_issues'},
            {elementId: 'navblue_tickets', dataKey: 'navblue_tickets'},
            {elementId: 'procedural_changes', dataKey: 'procedural_changes'},
            {elementId: 'fob_created_aog', dataKey: 'fob_created_aog'},
            {elementId: 'remarks_added', dataKey: 'remarks_created_com'},
            {elementId: 'aog', dataKey: 'aog'},
            {elementId: 'non-standard-flight', dataKey: 'non_standard_flights'},
            {elementId: 'naifr', dataKey: 'naifr'},
            {elementId: 'comat_flights', dataKey: 'comat_flights'}
        ]

        fetch(`view/selection/?shift_date=${selectedDate}&shift_type=${selectedShift}`)
            .then(response => response.json())
            .then(data => {
                if (!data.error && data.data.length >0) {
                    handoverCard.style.display = 'block';

                    const handoverData = data.data[0]
                    elements.forEach(item => {
                        const element = document.getElementById(item.elementId)
                        // const element = document.getElementById('aog');
                        const elementType = element.tagName;


                        if (elementType === "INPUT" && element.type === 'checkbox') {
                            element.checked = handoverData[item.dataKey]
                        }

                        if (item.elementId === "aog") {
                            if (handoverData.aog.length > 0) {
                                    element.innerHTML = '';
                            }
                            for (const aog_item of handoverData.aog) {

                                const newRow = document.createElement("tr");

                                newRow.innerHTML = `
                                <td><input type="text" class="form-control handover-form-control" readonly value="${aog_item.tail}"></td>
                                <td><input type="text" class="form-control handover-form-control" readonly value="${aog_item.fob}"></td>
                                                        <td><textarea class="form-control handover-form-control" rows="2" readonly>${aog_item.issue}</textarea></td>
                                `
                                element.appendChild(newRow);
                            }
                        } else if (item.elementId === "non-standard-flight") {
                            if (handoverData.non_standard_flights.length > 0) {
                                    element.innerHTML = '';
                            }
                            for (const flight of handoverData.non_standard_flights) {

                                const newRow = document.createElement("tr");

                                newRow.innerHTML = `
                                    <td><input type="text" class="form-control handover-form-control" readonly value="${flight.flight}"></td>
                                    <td><input type="text" class="form-control handover-form-control" readonly value="${flight.alternate}"></td>
                                    <td><textarea class="form-control handover-form-control" rows="2" readonly>${flight.extra}</textarea></td>
                                    `
                                element.appendChild(newRow);
                            }
                        } else if (item.elementId === "naifr") {
                            if (handoverData.naifr.length > 0) {
                                    element.innerHTML = '';
                            }
                            for (const naifr of handoverData.naifr) {

                                const newRow = document.createElement("tr");

                                newRow.innerHTML = `
                                    <td><input type="text" class="form-control handover-form-control" readonly value="${naifr.flight}"></td>
                                    <td><textarea class="form-control handover-form-control" rows="2" readonly>${naifr.destination}</textarea></td>
                                    `
                                element.appendChild(newRow);
                            }
                        } else if (item.elementId === "comat_flights") {
                            if (handoverData.comat_flights.length > 0) {
                                    element.innerHTML = '';
                            }
                            for (const comat of handoverData.comat_flights) {

                                const newRow = document.createElement("tr");

                                newRow.innerHTML = `
                                    <td><input type="text" class="form-control handover-form-control" readonly value="${comat.flight}"></td>
                                    <td><textarea class="form-control handover-form-control" rows="2" readonly>${comat.remark}</textarea></td>
                                    `
                                element.appendChild(newRow);
                            }
                        }

                        element.value = handoverData[item.dataKey];
                    })


                } else {
                    console.log("No Data Found!")
                    handoverCard.style.display = 'none';
                    const errorMessage = document.createElement('p');
                    errorMessage.innerText = "No Handover Found for that date and shift type";
                    errorMessage.classList.add('alert', 'alert-danger', 'mb-2');
                    errorMessage.style.marginBottom = "-0.5rem";
                    handoverSelector.prepend(errorMessage);

                }

            })
    }





}


const currentPage = window.location.pathname;
if (currentPage.startsWith("/handover/create")) {
    window.handover = new HandoverHandler();
} else if (currentPage.startsWith("/handover/view")) {
    window.handover_viewer = new HandoverViewHandler()

}
