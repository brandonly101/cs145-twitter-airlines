var Twit = require('twit');

var async = require('async');
var utf8 = require('utf8');

var excelbuilder = require('msexcel-builder');
var workbook = excelbuilder.createWorkbook('./', 'data.xlsx');

var T = new Twit({
  consumer_key:         'PG8wBb9aLTh76OsHoJ3nd0QRr',
  consumer_secret:      'jSEQCYEdiBzXafycqIqgA6kDZYaQ5YePpnpLAkkzqkZM4xJYUD',
  access_token:         '861666156-6fCsZg6nbFXMhMt2RliLXxVhcN5ga7hE1Ot5EWSp',
  access_token_secret:  'PXt3vuguz5FoCbRZGSYl2QN31I4HVi45bG9VlUB7u9S94',
  timeout_ms:           60*1000,
});

// we will look at 5 tweets from 5 different days (25 total)
// each tweet contains headers:
// 'date', 'author', 'predicted sentiment', 'observed sentiment', 'text'
var sheet = workbook.createSheet('sheet', 5, 30);
var headers = ['', 'Date', 'Author', 'Predicted Sentiment', 'Observed Sentiment', 'Text'];

for (var i = 1; i < 6; i++) {
    sheet.set(i, 1, headers[i]);
    sheet.align(i, 1, 'center');
    sheet.width(i, 20);
}

sheet.width(5, 180);

var queries = [
    ['2016-11-19', '2016-11-20'],
    ['2016-11-20', '2016-11-21'],
    ['2016-11-21', '2016-11-22'],
    ['2016-11-22', '2016-11-23'],
    ['2016-11-23', '2016-11-24']
];

async.map(queries, (query, callback) => {
    var params = {
        q: '@americanair',
        since: query[0],
        until: query[1],
        exclude: 'retweets',
        result_type: 'recent',
        count: 5
    };

    T.get('search/tweets', params, function(err, data, response) {
        if (err) callback(err);

        var size = data['statuses'].length;
        var arr = [];

        for (var i = 0; i < size; i++) {
            var obj = data['statuses'][i];

            var created_at = obj['created_at'];
            var user = obj['user']['name'];
            var text = utf8.encode(obj['text']);
            arr.push({
                created_at : created_at,
                user : user,
                text : text
            });
        }
        console.log('done with this section');
        callback(null, arr);
    });

}, (err, done) => {
    if (err) throw err;

    var row = 2;
    for (var i = 0; i < done.length; i++) {

        for (var j = 0; j < done[i].length; j++) {
            sheet.set(1, row, done[i][j]['created_at']);
            sheet.set(2, row, done[i][j]['user']);
            sheet.set(5, row, done[i][j]['text']);
            row++;
        }

        row++;
    }

    workbook.save(function(err){
    	if (err)
    		throw err;
    	else
    		console.log("workbook successfully created");
    });
});
