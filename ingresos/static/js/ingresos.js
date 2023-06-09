let dataTable;
let dataTableIsInitialized = false;

const dataTableOptionsDiego={
    columnDefs:[
        {className: "centeresDiego", targets:[0,1,2,3]},
    ],
    pageLenght : 4,
    destroy : true,
};

const initDataTable=async()=>{
    if(dataTableIsInitialized){
        dataTable.destroy();
    }
    await listFacturas();
    dataTable=$('#datatable-ingresos').dataTable({dataTableOptionsDiego});
    dataTableIsInitialized = true;

};

const listFacturas = async() =>{
    try{
        const response=await fetch('http://0.0.0.0:8000/ingresos/jsoningresos/');
        const data=await response.json();
        let content=``;
        console.log(data);
        data.listaIngresos.forEach((factura,index)=>{ // listaFacturas es el json que proviene de django
            content+=`
            <tr>
            <td>${index+1}</td>
            <td>${factura.nombreCaja}</td>
            <td>${factura.empresaIngreso}</td>
            <td>${factura.conceptoIngreso}</td>
            <td>${factura.valorIngreso}</td>
            <td>${factura.fecha}</td>
            <td>${factura.descripcion}</td>
            </tr>
            `;

        });
        tableBody_ingresos.innerHTML = content;
        // tableBody_programer es la etiqueta del cuerpo de la tabla


    }catch(ex){
        alert(ex);

    }

};


window.addEventListener("load",async() => {
    await initDataTable();

});