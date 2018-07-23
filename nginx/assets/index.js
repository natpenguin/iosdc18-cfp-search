let proposalsMaster = [];

// 検索フィールド
const searchField = new Vue({
    el: '#searchCondition',
    data: {
        searchWord: '',
        isAdopt: false
    },
    watch: {
        searchWord: 'filter',
        isAdopt: 'filter'
    },
    methods: {
        filter: function(event) {
            let text = this.searchWord;
            let isAdoptValue = this.isAdopt;
            let isKeywordMatch = function(value) {
                if (text.length > 0) {
                    let regText = new RegExp(text.trim(), 'i')
                    return regText.test(value.title) ||
                        regText.test(value.user) ||
                        regText.test(value.twitter_id) ||
                        regText.test(value.talk_type);
                } else {
                    return true;
                }
            };
            let isAdopted = function(value) {
                if (isAdoptValue) {
                    return value.is_adopted === true;
                } else {
                    return true;
                }
            };
            let filteredData = proposalsMaster.filter(value =>
                isKeywordMatch(value) && isAdopted(value)
            );
            proposalsInstance.proposals = filteredData;
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
             if (pros.is_adopted) {
                found.is_adopted  = pros.is_adopted;
                found.description = pros.description;
                found.detail_url  = pros.detail_url;
             }
        } else {
            proposals.push(pros);
        }
    });

    proposalsMaster = proposals;
    proposalsInstance.proposals = proposals;
})
