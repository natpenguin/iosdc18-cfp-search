let proposalsMaster = [];

// 検索フィールド
const searchField = new Vue({
    el: '#searchField',
    methods: {
        filter: function(event) {
            let text = event.target.value;
            if (text.length > 0) {
                let regText = new RegExp(text.trim(), 'i')
                let filteredData = proposalsMaster.filter(
                    value => 
                    regText.test(value.title) ||
                    regText.test(value.user) ||
                    regText.test(value.twitter_id) ||
                    regText.test(value.talk_type)
                );
                proposalsInstance.proposals = filteredData;
            } else {
                proposalsInstance.proposals = proposalsMaster;
            }
        }
    }
});

// プロポーザル一覧
const proposalsInstance = new Vue({
    el: '#proposals',
    data: {
        proposals: [],
        isLoaded: false
    },
    methods: {
        loaded: function(event) {
            this.isLoaded = true;
        }
    }
})

// プロポーザル一覧を読み込み
axios.get('/api')
.then(function (response) {

    const proposals = []; // mutable

    // Aggrigate the same talk types
    response.data.forEach(pros => {

        const found = proposals.find(element =>
            element.user        == pros.user
         && element.title       == pros.title
         && element.description == pros.description
        );

        if (found) {
             const talk_type = found.talk_type + ' / ' + pros.talk_type;
             found.talk_type = talk_type.split(' / ').sort().join(' / ');
        } else {
            proposals.push(pros);
        }
    });

    proposalsMaster = proposals;
    proposalsInstance.proposals = proposals;
})
