<template>
  <div>
    <p></p>
    <center>
      <table>
      <tr>
        <th scope="col">Estadistica</th>
        <th scope="col">Valor</th>
      </tr>
      <tr>
        <td scope="row"><b>usuarios</b></td>
        <td>{{statistics["cant. usuarios"]}}</td>
      </tr>
      <tr>
        <td scope="row">- administradores</td>
        <td>{{statistics["cant. administradores"]}}</td>
      </tr>
      <tr>
        <td scope="row">- operadores</td>
        <td>{{statistics["cant. operadores"]}}</td>
      </tr>
      <tr>
        <td scope="row"><b>denuncias</b></td>
        <td>{{statistics["cant. denuncias"]}}</td>
      </tr>
      <tr>
        <td scope="row">- denuncias con seguimientos</td>
        <td>{{statistics["cant. denuncias con seguimientos"]}}</td>
      </tr>
      <tr>
        <td scope="row">- denuncias sin seguimientos</td>
        <td>{{statistics["cant. denuncias sin seguimientos"]}}</td>
      </tr>
      <tr>
        <td scope="row"><b>rutas de evacuacion</b></td>
        <td>{{statistics["cant. rutas de evacuacion"]}}</td>
      </tr>
      <tr>
        <td scope="row"><b>zonas inundables</b></td>
        <td>{{statistics["cant. zonas inundables"]}}</td>
      </tr>
      <tr>
        <td scope="row"><b>puntos de encuentro</b></td>
        <td>{{statistics["cant. puntos de encuentro"]}}</td>
      </tr>
    </table>
    </center>
  </div>
</template>
<style>
  table {     font-family: "Lucida Sans Unicode", "Lucida Grande", Sans-Serif;
    font-size: 12px;    margin: 45px;     width: 480px; text-align: left;    border-collapse: collapse; }

  th {     font-size: 13px;     font-weight: normal;     padding: 8px;     background: #b9c9fe;
    border-top: 4px solid #aabcfe;    border-bottom: 1px solid #fff; color: #039; }

  td {    padding: 8px;     background: #e8edff;     border-bottom: 1px solid #fff;
    color: #669;    border-top: 1px solid transparent; }

  tr:hover td { background: #d0dafd; color: #339; }
</style>
<script>
import axios from 'axios';
const SERVER_URL = "https://admin-grupo13.proyecto2021.linti.unlp.edu.ar/api";
//const SERVER_URL = "https://127.0.0.1:5000/api"

export default {
  name: 'Statistics',
  data: () => ({
        statistics: [],
    }),
  props: {
    msg: String
  },
  methods: {
    async get() {
        axios.get(SERVER_URL+'/estadisticas/')
              .then(response => {
              // JSON responses are automatically parsed.
                this.statistics = response.data;
                console.log(response)
              })
              .catch(e => {
                console.log(e)
              })
    }
  },
  created() {
    this.statistics = this.get()
  }

}

</script>