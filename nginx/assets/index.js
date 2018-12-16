let proposalsMaster = [];

// 検索フィールド
const searchField = new Vue({
    el: '#searchCondition',
    data: {
        searchWord: '',
        isAdopt: true,
        isNotAdopt: true,
        eventType: undefined // (orecon|rejectcon)
    },
    watch: {
        searchWord: 'filter'
    },
    methods: {
        filter: function(event) {
            let text = this.searchWord;
            let isAdoptValue = this.isAdopt;
            let isNotAdoptValue = this.isNotAdopt;
            let eventType = this.eventType;
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
            let filteredData = [];
            if (eventType) {
                let isMatchEvent = function(proposal) {
                    return (eventType === 'orecon' && proposal.is_adopted_orecon === true)
                        || (eventType === 'rejectcon' && proposal.is_adopted_rejectcon === true);
                };
                filteredData = proposalsMaster.filter(proposal =>
                    isKeywordMatch(proposal) && isMatchEvent(proposal)
                );
            } else {
                let isAdopted = function(value) {
                    if (isAdoptValue) {
                        return value.is_adopted === true;
                    } else {
                        return false;
                    }
                };
                let isNotAdopted = function(value) {
                    if (isNotAdoptValue) {
                        return value.is_adopted === false;
                    } else {
                        return false;
                    }
                };
                filteredData = proposalsMaster.filter(value =>
                    isKeywordMatch(value)
                        && (isAdopted(value) || isNotAdopted(value))
                );
            }
            proposalsInstance.proposals = filteredData;
        }
    }
});

// プロポーザル一覧
const proposalsInstance = new Vue({
    el: '#proposals',
    data: {
        proposals: undefined
    }
})

// プロポーザル一覧を読み込み
axios.get('/api')
    .then(function (response) {
        let proposals = response.data.map(proposal => {
            const dict = {
                'LT': 'LT（5分）',
                'LT_R': 'iOSDCルーキーズ LT（5分）',
                '15m': 'レギュラートーク（15分）',
                '30m': 'レギュラートーク（30分）',
                'iOS': 'iOSエンジニアに聞いて欲しいトーク（30分）',
            }
            proposal.talk_type = proposal.talk_types.map(talk_type => dict[talk_type]).join(' / ')
            return proposal
        });
        proposalsMaster = proposals;
        proposalsInstance.proposals = proposals;
    })
