const APIGET = 'http://localhost:5001'
Vue.component('reserve-field', {
    props: ['records'],
    methods: {
        updateDrama: function (id) {
            this.$parent.$emit('app').updateDrama(id)
        },
    },

    //この下にdata,methodを入れる

    data: () => ({
        message: '',
        isError: false,
        entryName: '',
        entryDistance: '',
        hiddenId: '',
        name: '',
        day: '',
        error_name: false,
        error_day: false,
        result: []
    }),
    methods: {
        errorClear: function() {
            this.error_name = false
            this.error_day = false
        },
        inputClear: function() {
            this.name = ''
            this.day = ''
            this.errorClear()
        },
        inputCheck: function() {
            this.error_name = this.name == '' ? true : false //条件演算子
            this.error_day = this.day == '' ? true : false
            return (this.error_name || this.error_day) ? false : true
        },
        //Object.assignでオブジェクトをマージ(まとめる)ことができる
        //dataの項目をすべて初期値にする
        //this.$options.dataは元のdataメソッドを再び呼び出すため
        allClear: function() {
            Object.assign(this.$data, this.$options.data.call(this))
        },
        //RestAPIを用いる実行を容易に実装するためのaxios
        //thenでresolve側の処理、catchでreject側の処理
        getDrama: function () {
            this.errorClear()
            axios
                .get(`${APIGET}`)
                .then(res => (this.result = res.data.result))
                .catch((err) => {
                    this.message = 'データの取得に失敗しました'
                    this.isError = true
                })
        },
        //inputCheckに引っかからないならreturn
        //alertでポップアップだして押さずにサイト消してもデータに入ってもらうためのasync-await
        addDrama: async function () {
            if(!this.inputCheck()) return
            await axios
                .post(`${APIGET}`,{name: this.name, day: this.day})
                .then(res => (this.result = res.data.result))
                .catch((err) => {
                    this.message = 'データの登録に失敗しました'
                    this.isError = true
                })
            alert('予約完了！予約内容をラインで送信しました！')
            this.inputClear()
        },
        updateDrama: async function (id) {
            if(!this.inputCheck()) return
            await axios
                .put(`${APIGET}`,{id: id, name: this.name, day: this.day })
                .then(res => (this.result = res.data.result))
                .catch((err) => {
                    this.message = 'データの更新に失敗しました'
                    this.isError = true
                })
            alert('予約変更完了！変更内容をラインで送信しました！')
            this.inputClear()
        },
    },

    template: `<main>
                    <style>
                        h1{color: #00a0dc}
                    </style>
                    <h2>Reservation</h2>
                    <br>
                    <label>ドラマタイトル</label>
                    <input type="text" v-model="name">
                    <span v-if="error_name" style="color:red">タイトル名が入力されていません</span>
                    <br>
                    <label>放送日時</label>
                    <input type="datetime-local" v-model="day">
                    <span v-if="error_day" style="color:red">放送日時が入力されていません。</span>
                    <br>
                    <button v-on:click="allClear">
                        <font size="2">CLEAR</font>
                    </button>
                    <button v-on:click="getDrama">
                        <font size="2">GET</font>
                    </button>
                    <button v-on:click="addDrama">
                        <font size="2">ADD</font>
                    </button>
                    <drama-table v-bind:records="result"></drama-table>
                    <!--枠線あり、１重線 -->
                    <table border="1" style="border-collapse: collapse">
                        <tr style="background-color:lightblue">
                            <th style="min-width:200px">ドラマタイトル</th>
                            <th style="min-width:100px">放送日時</th>
                            <th style="min-width:50px">修正</th>
                        </tr>
                        <tr v-for="rec in result" v-bind:key="rec._id">
                            <td>{{rec.name}}</td>
                            <td>{{rec.day}}</td>
                            <td style="text-align:center">
                                <button style="background-color:lightgreen;border-radius:3px;width:100%;" v-on:click="updateDrama(rec._id)">FIX</button>
                            </td>
                        </tr>
                    </table>

                </main>
                `

})
