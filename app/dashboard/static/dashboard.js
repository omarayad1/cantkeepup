function loadUserCommandsDB(){

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

        updateItem: function(updatingCommand) { },

        deleteItem: function(deletingCommand) {
        }

    };
    window.db = db
}

function loadUserCommandsJsGrid() {

    $("#userCommands").jsGrid({
        height: "auto",
        width: "100%",
        inserting: true,
        filtering: false,
        editing: false,
        sorting: false,
        paging: false,
        autoload: true,
        pageSize: 15,
        pageButtonCount: 5,
        deleteConfirm: "Do you really want to delete this command?",
        controller: db,
        fields: [
            { name: "cmd_id", title: "Command ID", align: "left", type: "text", width: 50 },
            { name: "name", title: "Name", type: "text", width: 50 },
            { name: "url", title: "URL", type: "text", width: 150 },
            { type: "control" }
        ]
    });
 
    $("#userCommands").jsGrid({
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
        }
    });
}
