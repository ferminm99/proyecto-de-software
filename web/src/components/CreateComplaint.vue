<template>

  <div class="container" style="padding:25px;width: 100%;height: 100%;position: relative;">
    <!--
    <div class="col-12 col-md-4  py-2">
    <div class="card w-100 mt-3 border-secondary border-radius-50" style="width: 18rem;">
    -->

    <div class="card w-80" style="position: absolute; padding:5px">
      <div class="row " id="columna">
        <div class="col-md-6">
            <label for="title" class="col-form-label text-color">Titulo</label>
            <input id="titleInput"  class="form-control" type="text" name="title" v-model="form.title" placeholder="Escriba el titulo">
        </div>
        <div class="col-md-6">
            <label for="state" class="col-form-label text-md-left text-color">Categoria</label>
            <select id="categoryInput" class="form-control" name="category" v-model="form.category" placeholder="Estado de la denuncia">   
              <option v-for="category in categories.categories" v-bind:key="category.id" v-bind:value="category.id">{{category.type}}</option>
            </select>
        </div>
        <div class="col-md-12">
            <label for="description" class="col-form-label text-color">Descripcion</label>
            <textarea placeholder="Escriba la descripcion" id="descriptionInput" v-model="form.description" class="form-control" name="description" rows="3"  ></textarea>
        </div>
        <hr>
        <div class="col-md-6">
            <label for="firstname" class="col-form-label text-color">Nombre denunciante</label>
            <input id="firstnameInput" placeholder="Escriba su nombre" v-model="form.firstname" class="form-control" type="text" name="firstname" >
        </div>
        <div class="col-md-6">
            <label for="lastname" class="col-form-label text-color">Apellido denunciante</label>
            <input id="lastnameInput" v-model="form.lastname" placeholder="Escriba su apellido" class="form-control" type="text" name="lastname" >
        </div>
        <div class="col-md-6">
            <label for="telephone" class="col-form-label text-color">Telefono</label>
            <input id="telephoneInput" v-model="form.telephone" placeholder="Escriba su telefono" class="form-control" name="telephone"  >
        </div>
        <div class="col-md-6">
            <label for="email_address" class="col-form-label text-color">E-Mail</label>
            <input type="email" id="emailInput" v-model="form.email" placeholder="Escriba su email" class="form-control" name="email"  >
        </div>
        <div class="col-md-12" style="padding: 15px">
          <h5> Coordenadas: </h5>
        </div>
        <div class="col-md-6">
            <label for="latitude" class="col-form-label text-color">Latitud</label>
            <input id="latitudeInput" v-model="form.latitudeInput" class="form-control" type="text" name="latitude"  readonly required>
        </div>
        <div class="col-md-6">
            <label for="length" class="col-form-label text-color">Longitud</label>
            <input id="lengthInput" v-model="form.lengthInput" class="form-control" type="text" name="length"  readonly required>
        </div>
      </div>    

          <!-- Edicion de cordenadas -->
     
         
      
          <!-- Fin coordenadas -->
          
          
        <br>
        <div id="mimapa" style="height: 300px; width:100% ; z-index: 0;"></div>
      
          <div style="padding: 5px" class="container">
            
              <a class="btn btn-md btn-primary col-md-6" v-on:click="create()">
                  Crear
              </a>
              
              <a class="btn btn-md btn-danger col-md-6 justify-center" v-on:click="back()">
                  Cancelar
              </a>
            
  
          </div>
      </div>
        
  </div>
<!--
  </div>
</div>
-->
</template>
<script>
import leaflet from "leaflet";
import axios from 'axios';
import { createToast } from 'mosha-vue-toastify';
import 'mosha-vue-toastify/dist/style.css';
const SERVER_URL = "https://127.0.0.1:5000"; 

export default {
  name: 'CreateComplaint',
  data: () => ({
   
    form: {
      email: '',
      title: '',
      description: '',
      firstname: '',
      lastname: '',
      telephone: '',
      latitudeInput: '',
      lengthInput: '',
      category: '',
    }, 
      
    categories: []
  }),

  mounted() {
    
    var mymap = leaflet.map('mimapa').setView([-34.92114,-57.95502], 13);
    leaflet.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
      maxZoom: 25,
      attribution: 'Datos del mapa de &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a>, ' + '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' + 'Imágenes © <a href="https://www.mapbox.com/">Mapbox</a>', 
      id: 'mapbox/streets-v11'
    }).addTo(mymap);

    var marker = leaflet.marker([ (document.getElementById('latitudeInput').value), document.getElementById('lengthInput').value]).addTo(mymap);
              
    mymap.on('click', e =>{
      let latLng = mymap.mouseEventToLatLng(e.originalEvent);  
      let result =confirm(`Desea agregar un Punto de encuentro en esta ubicacion: ${latLng}` );
      if (result){
        mymap.removeLayer(marker);
        marker = leaflet.marker(mymap.mouseEventToLatLng(e.originalEvent)).addTo(mymap); 
        document.getElementById('latitudeInput').value=( latLng.lat);
        document.getElementById('lengthInput').value=(latLng.lng);
        this.form.lengthInput = latLng.lng;
        this.form.latitudeInput = latLng.lat;
   
      }
    }); 
    
  },
  methods: {  
    
    async get() {
      axios.get(SERVER_URL+'/api/denuncias/categories')
        .then(response => {
        // JSON responses are automatically parsed.

          this.categories = response.data;
          
        })
        .catch(e => {
          console.log(e)
        })
    },

    back() {
      
      window.location = "/";
      
    },
    create() {
        
        for (const prop in this.form) {
          //console.log(this.form.firstname);
          //console.log(!(/^[a-zA-ZÀ-ÿ\u00f1\u00d1]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d1]*)*[a-zA-ZÀ-ÿ\u00f1\u00d1]+$/).test(this.form.email));

          if (`${this.form[prop]}` == "") {
              createToast({title:'Error', description: 'No debe haber ningun campo vacio!'},{type:'danger'});
              return false;
          }
        }
       
        if (!(/^[a-zA-ZÀ-ÿ\u00f1\u00d1]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d1]*)*[a-zA-ZÀ-ÿ\u00f1\u00d1]+$/.test(this.form.firstname))
            || !(/^[a-zA-ZÀ-ÿ\u00f1\u00d1]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d1]*)*[a-zA-ZÀ-ÿ\u00f1\u00d1]+$/.test(this.form.lastname))) {
          createToast({title:'Error', description: 'El nombre o el apellido tienen un formato invalido!'},{type:'danger'});
          return false;
        }

        let splittedTelephone = this.form.telephone.split("-");
        let telephoneToCheck = '';
        let check = false;

        for (const prop in splittedTelephone) {
  
          if (`${splittedTelephone[prop]}` != null) {
              telephoneToCheck = telephoneToCheck + `${splittedTelephone[prop]}`;
              console.log(telephoneToCheck);
          }
          if((prop>0) && (check) ){
            check = true;
          }

        }

        if((/[^\d]/).test(telephoneToCheck) || (telephoneToCheck.length>20)){
          createToast({title:'Error', description: 'El formato deben ser solo numeros con un "-" de separacion y menos de 20 caracteres!'},{type:'danger'});
          return false;
        }else if(!check){
          createToast({title:'Error', description: 'El formato deben ser solo numeros con "-" de separacion!'},{type:'danger'});
          return false;
        }
        
        if ((/^[a-zA-ZÀ-ÿ\u00f1\u00d1]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d1]*)*[a-zA-ZÀ-ÿ\u00f1\u00d1]+$/).test(this.form.email)) {
          createToast({title:'Error', description: 'El email tiene un formato invalido!'},{type:'danger'});
          return false;
        }        


        const myJSON = { 
            "categoria_id": Number(this.form.category),
            "coordenadas": this.form.latitudeInput+", "+this.form.lengthInput,
            "apellido_denunciante": this.form.lastname,
            "nombre_denunciante": this.form.firstname,
            "telcel_denunciante": this.form.telephone,
            "email_denunciante": this.form.email,
            "titulo": this.form.title,
            "descripcion": this.form.description
        };

        axios.post(SERVER_URL+'/api/denuncias/',JSON.stringify(myJSON),{
            headers: {
              'Content-Type': 'application/json'
            }
          })
          .then(response => {
            
          // JSON responses are automatically parsed.
            createToast({title:'Exito', description: 'Se creo su denuncia, dentro de un tiempo sera revisada por los encargados!'},{type:'success'});
            window.location = "/";
            console.log(response);
            
          })
          .catch(e => {
            console.log(e)
          })

        
    },
    
  },
  created() {
    this.categories = this.get();

  },
}
</script>


