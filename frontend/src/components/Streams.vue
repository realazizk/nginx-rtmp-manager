<template>
    <div class="container">
        <table class="table table-bordered">
            <thead>
                <tr>
                    <th>{{$t('streamsp.streamname')}}</th>
                    <th>{{$t('streamsp.streamtype')}}</th>
                    <th>{{$t('streamsp.delete')}}</th>
		    <th>{{$t('streamsp.edit')}}</th>

                </tr>
            </thead>
            <tbody>
	      <tr v-for="(row, index) in streams">
		<td>{{ row.name }}</td>
		<td>{{ row.stype }}</td>
		<td><a @click="removeRow(row, index)">{{$t('streamsp.remove')}}</a></td>
		<td><a @click="editRow(row, index)">{{$t('streamsp.edit')}}</a></td>
	      </tr>
            </tbody>
        </table>

	<bootstrap-modal ref="editstream" :needHeader="true" :needFooter="false" size="large">
	    <div slot="title">
		{{$t('editstreammodal.title')}}
	    </div>
	    <div slot="body">
		<form action="">
		    <label for="currstream.name">{{$t('addstreammodal.url')}}</label>
		    <input type="text"   v-model="currstream.name" class="form-control" id="name" aria-describedby="basic-addon3">
		    <label for="currstream.stype">{{$t('addstreammodal.stype')}}</label>
		    <select :value="currstream.stype" v-model="currstream.stype"  class="form-control" id="stype">
			<option>video</option>
			<option>audio</option>
		    </select>
		    
		    <button type="submit" class="btn btn-default "  @click="editstream()">{{$t('addstreammodal.submit')}}</button>
		    
		</form>
	    </div>

	</bootstrap-modal>

	
    </div>

    
  </template>

<script>
import {API_URL} from '@/shared.js'
import auth from '@/auth'

export default {
  data() {
    return {
      streams: [],
      currstream: {
	stype: null,
	name: null,
	id: null
      }
    }
  },

  methods: {
    removeRow(row, index) {
      var vm = this
      this.$http.delete(
	API_URL + 'api/stream/' + row.id,
	{headers: auth.getAuthHeader()}
      ).then(
	response => {
	  vm.$delete(vm.streams, index)
	}, response => {
	  vm.$delete(vm.streams, index)
	})
    },

    editRow(row, index) {
      this.currstream = row
      this.opentheModals(index)
    },

    editstream (index) {
      let vm = this
      this.$http.patch(API_URL + 'api/stream/' + this.currstream.id,
		       this.currstream,
		       {headers: auth.getAuthHeader()}).then(
			 response => {
			   let resp = response.body
			   vm.$set(vm.streams, index, resp)
			   vm.$refs.editstream.close()
			 }
		       )

    },

    opentheModals() {
      this.$refs.editstream.open()
    },
    
  },
  
  created() {
    // grab user streams
    this.$http.get(API_URL + 'api/streams', {headers: auth.getAuthHeader()}).then(
      response => {
	let data = response.body
	this.streams = data
      })
  }
}
  
</script>


<style scoped>
</style>

