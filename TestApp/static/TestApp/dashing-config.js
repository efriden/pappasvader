/* global $, Dashboard */

var dashboard = new Dashboard();

dashboard.addWidget('clock_widget', 'Clock');

dashboard.addWidget('forecast_widget', 'Graph', {
	interval: 10000,
	getData: function () {
		var self = this;
		$.get('/forecast/', function (data) {
			$.extend(self.scope, {
				title: data.title,
				moreInfo: data.moreInfo,
				data: data.data,
				value: data.value,
				properties: { min: 'auto' }
			})
		});
	}
});

dashboard.addWidget('sun_widget', 'Knob', {
	getData: function () {
		var self = this;
		$.get('/sun/', function (data) {
			$.extend(self.scope, {
				title: data.title,
				data: data.data,
				value: data.value,
				moreInfo: data.moreInfo
			});
		})
	}
});

dashboard.addWidget('trello_widget', 'List', {
	color: 'steelblue',
	row: 1,
	getData: function () {
		var self = this;
		$.get('/trello/', function (data) {
			$.extend(self.scope, {
				title: data.title,
				moreInfo: data.moreInfo,
				updatedAt: data.updatedAt,
				data: data.data
			});
		});
	}
});

dashboard.addWidget('weather_widget', 'Number', {
	interval: 10000,
	getData: function () {
		var self = this;
		$.get('/weather/', function (data) {
			$.extend(self.scope, {
				title: data.title,
				moreInfo: data.moreInfo,
				updatedAt: data.updatedAt,
				detail: data.detail,
				value: data.value
			});
		});
	}
});
