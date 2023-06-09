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
    dataTable=$('#datatable-facturas').dataTable({dataTableOptionsDiego});
    dataTableIsInitialized = true;

};

const listFacturas = async() =>{
    try{
        const response=await fetch('http://0.0.0.0:8000/egresos/jsonfacturas/');
        const data=await response.json();
        let content=``;
        let content1=``;
        let valorTotal = 0;
        console.log(data);
        data.listaFacturas.forEach((factura,index)=>{ // listaPagoColaboradores es el json que proviene de django
            valorTotal = valorTotal + parseFloat(factura.valor);
            content+=`
            <tr>
            <td>${index+1}</td>
            <td>${factura.idproveedor}</td>
            <td>${factura.numeroFactura}</td>
            <td>${factura.valor}</td>
            <td>${factura.id_modoCompra}</td>
            <td>${factura.fechafactura}</td>
            <td>${factura.fechapago}</td>
            <td>${factura.id_caja}</td>
            </tr>
            `;
        });
        content1 =`
        <tr>
        <td>Total</td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>

       


        </tr>
        `;

        tableBody_facturas.innerHTML = content + content1;
        // tableBody_colaboradores_pago_resumen es la etiqueta del cuerpo de la tabla


    }catch(ex){
        alert(ex);

    }

};


window.addEventListener("load",async() => {
    await initDataTable();

});