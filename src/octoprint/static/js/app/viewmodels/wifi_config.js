function WifiConfigViewModel() {
    var self = this;

    self.ssids = ko.observableArray(undefined);
	this.selectedSSIDs = ko.observableArray(["Ham"]);       
	
	// Load all available countries /v1/countries
	self.loadSSIDs = function(callback) {
		// Let loading indicator know that there's a new loading task that ought to complete
		// self.loading.push(true);
 
		$.getJSON('/api/wificfg',
			function(data) {
				console.log("loaded countries")
				console.dir(data);
 
				self.ssids(data.ssids);
				// Let loading indicator know that this task has been completed
				// self.loading.pop();
				// Try to call success callback, which is loadUser if and only if all parallel processes have completed
				if (callback) {callback();}
			}
		);
	}
	

    self.joinExistingWifi = function() {
        if (!self.validData()) return;

        var data = {
            "ac": true,
            "user": self.username(),
            "pass1": self.password(),
            "pass2": self.confirmedPassword()
        };
        self._sendData(data);
    };

    self.keepInternalWifi = function() {
        $("#confirmation_dialog .confirmation_dialog_message").html("If you disable Access Control <strong>and</strong> your OctoPrint " +
            "installation is accessible from the internet, your printer <strong>will be accessible by everyone - " +
            "that also includes the bad guys!</strong>");
        $("#confirmation_dialog .confirmation_dialog_acknowledge").unbind("click");
        $("#confirmation_dialog .confirmation_dialog_acknowledge").click(function(e) {
            e.preventDefault();
            $("#confirmation_dialog").modal("hide");

            var data = {
                "ac": false
            };
            self._sendData(data, function() {
                // if the user indeed disables access control, we'll need to reload the page for this to take effect
                location.reload();
            });
        });
        $("#confirmation_dialog").modal("show");
    };

    self._sendData = function(data, callback) {
        $.ajax({
            url: API_BASEURL + "setup",
            type: "POST",
            dataType: "json",
            data: data,
            success: function() {
                self.closeDialog();
                if (callback) callback();
            }
        });
    }

    self.showDialog = function() {
        $("#wifi_config_dialog").modal("show");
		self.loadSSIDs();
    }

    self.closeDialog = function() {
        $("#wifi_config_dialog").modal("hide");
    }
}
