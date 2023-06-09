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
    dataTable=$('#datatable-pago_creditos').dataTable({dataTableOptionsDiego});
    dataTableIsInitialized = true;

};

const listFacturas = async() =>{
    try{
        const response=await fetch('http://0.0.0.0:8000/egresos/jsonpagocreditos/');
        const data=await response.json();
        let content=``;
        let content1=``;
        let valorTotal = 0;
        console.log(data);
        data.ListaPagoCreditos.forEach((factura,index)=>{ // listaPagoColaboradores es el json que proviene de django
            valorTotal = valorTotal + parseFloat(factura.valor);
            content+=`
            <tr>
            <td>${index+1}</td>
            <td>${factura.id_empresa}</td>
            <td>${factura.id_caja}</td>
            <td>${factura.valor}</td>
            <td>${factura.nombre_coop}</td>
            <td>${factura.fecha}</td>
            <td>${factura.mes_de_Pago}</td>
            <td>${factura.anio_de_pago}</td>
            <td>${factura.descripcion}</td>
         
            </tr>
            `;
        });
        content1 =`
        <tr>
        <td>Total</td>
        <td></td>
        <td></td>
        <td></td>
        <td>${valorTotal}</td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
       


        </tr>
        `;

        tableBody_pagoCreditos.innerHTML = content + content1;
        // tableBody_colaboradores_pago_resumen es la etiqueta del cuerpo de la tabla


    }catch(ex){
        alert(ex);

    }

};


window.addEventListener("load",async() => {
    await initDataTable();

});