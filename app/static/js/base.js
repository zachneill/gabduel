$(document).ready(function () {
    // Set CSRF token to avoid CSRF error when deleting post
    $.ajaxSetup({
        headers: {
            "X-CSRFToken": $("#csrf").val()
        }
    });
});

function deletePost(postId) {
    // Delete post
    $.ajax("/delete", {
        method: "POST",
        data: {postId: postId},
        success: function () {
            // Reloads page if successful
            location.reload()
        },
        error: function (error) {
            // Logs error to console if unsuccessful
            console.log(error["responseText"]);
        }
    });
}

$('#searchButton').on("click", function () {
    // Gets search query
    let query = $("#searchInput").val()
    if (query !== "") {
        // Redirects to search page
        window.location.href = `/search/${query}`;
    }
});
// Service worker
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function () {
        navigator.serviceWorker.register("/sw.js").then(function (registration) {
        console.log('ServiceWorker registration successful with scope: ', registration.scope);
    }, function (err) {
        console.log('ServiceWorker registration failed: ', err);
        });
    });
}
// For populating the modal with the post data
$("#postModal").on("show.bs.modal", function (event) {
    // Update views count
    let button = $(event.relatedTarget)
    let postId = button.data("postid")
    $.ajax("/post/updateViews", {
        method: "POST",
        data: {postId: postId},
        success: function () {
            // Console log if successful
            console.log("Views updated!")
        },
        error: function (error) {
            // Logs error to console if unsuccessful
            console.log(error["responseText"]);
        }
    })

    $("#postTitle").text($("#title_"+postId).text())
    $("#postContent").text($("#content_"+postId).text())
    $("#author1").text("Support "+ $("#author1_FN_"+postId).text())
    $("#author1").data("author", $("#postModalLauncher_"+postId).data("author1_id"))
    $("#author1").data("postid", postId)
    $("#author2").text("Support "+ $("#author2_FN_"+postId).text())
    $("#author2").data("author", $("#postModalLauncher_"+postId).data("author2_id"))
    $("#author2").data("postid", postId)
});

$(".supportButton").on("click", function () {
    // Gets post id and support id
    let postId = $(this).data("postid")
    let supportId = $(this)[0].id === "author1" ? 1 : 2
    let authorId = $(this).data("author")
    let otherAuthorId = supportId === 1 ?
        $("#postModalLauncher_"+postId).data("author2_id") : $("#postModalLauncher_"+postId).data("author1_id")
    let mindChanged = 0
    // Check if there already is a green border around a previously supported author
    if ($('#avatar_'+otherAuthorId).hasClass("supported")) {
        mindChanged = 1
    }
    $.ajax("/post/support", {
        method: "POST",
        data: {postId: postId, supportId: supportId, mindChanged: mindChanged},
        success: function () {
            // Closes modal if successful
            $("#postModal").modal("hide")
            // Add a green border around supported author's image
            if (mindChanged === 1) {
                $("#avatar_"+otherAuthorId).removeClass("supported")
                $("#avatar_"+authorId).addClass("supported")
            } else {
                $("#avatar_"+authorId).addClass("supported")
            }
        },
        error: function (error) {
            // Logs error to console if unsuccessful
            console.log(error["responseText"]);
        }
    })
})