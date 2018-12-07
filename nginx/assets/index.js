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

    const proposals = []; // mutable

    // Aggrigate the same talk types
    response.data.forEach(pros => {

        const found = proposals.find(element =>
            element.user        == pros.user
         && element.title       == pros.title
         && element.description == pros.description
        );

        pros.orecon_form_url = "https://docs.google.com/forms/d/e/1FAIpQLSfFaoVGH__Ck-CzdnH83ZC_1PlFewXsJmoEe68mhrNfeRLA4w/viewform?entry.1898580758=" + pros.detail_url;

        if (found) {
             const talk_type = found.talk_type + ' / ' + pros.talk_type;
             found.talk_type = talk_type.split(' / ').sort().join(' / ');
             if (pros.is_adopted || pros.is_adopted_rejectcon || pros.is_adopted_orecon) {
                found.is_adopted           = pros.is_adopted;
                found.is_adopted_orecon    = pros.is_adopted_orecon;
                found.is_adopted_rejectcon = pros.is_adopted_rejectcon;
                found.description          = pros.description;
                found.detail_url           = pros.detail_url;
                found.orecon_form_url      = pros.orecon_form_url;
                found.video_url            = pros.video_url;
             }
        } else {
            proposals.push(pros);
        }
    });

    proposalsMaster = proposals;
    proposalsInstance.proposals = proposals;
})
