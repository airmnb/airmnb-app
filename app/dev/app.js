var app = angular.module('app', []);

app.service('session', function SessionFactory($http, $window, $q) {
	var deferred = $q.defer();
	var svc = {
		promise: deferred.promise,
		session: null
	};
	var localStorage = $window.localStorage;
	var sessionToken = null;
	try {
		var ses = JSON.parse(localStorage.getItem('amb_session'));
		console.log('loaded session from local storage', ses);
		sessionToken = ses['sessionToken'];
	} catch (e) {
		console.log('session not found or corrupted');
		localStorage.removeItem('abs_session');
	}
	var headers = sessionToken ? {'Authorization': 'Bearer ' + sessionToken} : {};
	console.log('about to call /session with headers as', headers);
	$http.get('/sys/whoami', {headers: headers}).then(function(response) {
		console.log('log succeeded', response.data);
		var ses = response.data;
		svc.session = ses;
		var saved = angular.extend({}, ses);
		delete saved.user;
		localStorage.setItem('amb_session', JSON.stringify(saved));
		deferred.resolve(ses.user);
	}, function(response) {
		console.log('error', response);
		if (response.status === 401) {
			var ses = response.data;
			svc.session = ses
			localStorage.setItem('amb_session', JSON.stringify(ses));
			deferred.resolve(null);
		} else {
			deferred.reject(response)
		}
	});
	return svc;
});

app.factory('authHeaderInterceptor', function($window) {
	return {
		request: function(config) {
			console.log('intercetor is working', config);
			config.headers = config.headers || {};
			var localStorage = $window.localStorage;
			var ses = localStorage.getItem('amb_session');
			if (ses && ses.sessionToken) {
				console.log('session is valid', session.session);
				config.headers['Authorization'] = 'Bearer ' + ses.sessionToken;
			}
			console.log('interceptor updated config:', config);
			return config;
		}
	};
});

app.config(function($httpProvider) {
	console.log('app.config is running to add interceptors');
	$httpProvider.interceptors.push('authHeaderInterceptor');
});

app.controller('MainCtrl', function($scope, $http, $window, session) {
	$scope.promise = session.promise;
	window.promise = session.promise;
	$scope.isLoading = true;
	console.log('session service is', session);
	session.promise.then(function(user) {
		console.log('session promise resolved, user is', user);
		$scope.user = user;

	}, function() {
		console.log('session promise rejected');
	}).finally(function() {
		$scope.isLoading = false;
	});

	$scope.getLink = function(key) {
		if ($scope.isLoading) {
			return null;
		}
		switch (key) {
		case 'facebook':
		case 'google':
			return '/sys/login?use=' + key + '&session_id=' + session.session.sessionId;
		default:
			return null;
		}
	};
	$scope.logout = function() {
		$window.localStorage.removeItem('amb_session');
		alert('bye');
	};
});
