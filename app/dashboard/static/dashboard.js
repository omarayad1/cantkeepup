function loadUserCommandsDB(){

}

function loadUserCommandsJsGrid() {

    var db = {

        loadData: function(filter) {
            return $.getJSON($SCRIPT_ROOT + '/dashboard/_loadusercommands', 
                filter).fail(function(response, status, error) {
                    alert('loading Failed:\n'+response.responseText);
                });
        },


        insertItem: function(insertingCommand) {
            return $.getJSON($SCRIPT_ROOT + '/dashboard/_addusercommand', 
                insertingCommand, function(data) {
                    alert('added successfully');
                }).fail(function(response, status, error) {
                    alert('Insertion Failed:\n'+response.responseText);
                });
        },

        updateItem: function(updatingCommand) { 
            return $.getJSON($SCRIPT_ROOT + '/dashboard/_updateusercommand', 
                updatingCommand, function(data) {
                    alert('updated successfully');
                }).fail(function(response, status, error) {
                    alert('Update Failed:\n'+response.responseText);
                });
        },

        deleteItem: function(deletingCommand) {
            return $.get($SCRIPT_ROOT + '/dashboard/_deleteusercommand', 
                deletingCommand, function(data) {
                    alert('deleted successfully');
                }).fail(function(response, status, error) {
                    alert('deletion Failed:\n'+response.responseText);
                });
        }

    };
    window.db = db

    $("#userCommands").jsGrid({
        height: "auto",
        width: "100%",
        inserting: true,
        filtering: false,
        editing: true,
        sorting: false,
        paging: false,
        autoload: true,
        pageSize: 15,
        pageButtonCount: 5,
        deleteConfirm: "Do you really want to delete this command?",
        controller: db,
        fields: [
            { name: "cmd_id", title: "Command ID", editing: false, type: "text", width: 50 },
            { name: "name", title: "Name", type: "text", width: 50 },
            { name: "url", title: "URL", type: "text", width: 150 },
            { type: "control" }
        ],
        onItemInserting: function(args) {
            errorMsg = "";
            if(args.item.cmd_id === "")
                errorMsg = errorMsg + 'Command ID is empty!\n'
            if(args.item.name === "")
                errorMsg += 'Name is empty!\n'
            if(args.item.url === "")
                errorMsg += 'URL is empty!\n'
            if(errorMsg != "") {
                alert('Errors:\n'+errorMsg);
                args.cancel = true;
            }
        },
        onItemUpdating: function(args) {
            errorMsg = "";
            if(args.item.name === "")
                errorMsg += 'Name is empty!\n'
            if(args.item.url === "")
                errorMsg += 'URL is empty!\n'
            if(errorMsg != "") {
                alert('Errors:\n'+errorMsg);
                args.cancel = true;
            }
        }
    });
 }
