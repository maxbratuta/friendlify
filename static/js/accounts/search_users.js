document.addEventListener("DOMContentLoaded", function () {
    const friendSearchbar = document.getElementById("friend_searchbar");
    const searchResultsDropdown = document.getElementById("search_results_dropdown");

    let debounceTimer;

    friendSearchbar.addEventListener("input", function () {
        clearTimeout(debounceTimer);

        const query = this.value;

        if (query.length >= 3) {
            debounceTimer = setTimeout(function () {
                friendSearchbar.classList.remove("with-results");

                // fetch(`/search_users/?q=${query}`)
                // fetch(`/users/search/?q=${query}`)
                fetch(`/users/search/?q=${query}`)
                    .then((response) => response.json())
                    .then((data) => {
                        searchResultsDropdown.innerHTML = "";

                        if (data.data.length === 0) {
                            friendSearchbar.classList.add("with-results");

                            const noResultsMessage = document.createElement("div");

                            noResultsMessage.classList.add("dropdown-item");
                            noResultsMessage.innerHTML = "No results found";

                            searchResultsDropdown.appendChild(noResultsMessage);
                        } else {
                            data.data.slice(0, 5).forEach((user) => {
                                friendSearchbar.classList.add("with-results");

                                const listItem = document.createElement("a");

                                listItem.classList.add("dropdown-item");
                                listItem.href = user.ref_link;

                                listItem.innerHTML = `
                                  <div class="d-flex flex-row justify-content-between align-items-center rounded">
                                    <div class="d-flex flex-row align-items-center">
                                        <div class="user-avatar w-fit-content h-fit-content m-1 bg-white border rounded-circle small-avatar">
                                          ${
                                            user.avatar
                                              ? `<img 
                                                    src="${user.avatar}" 
                                                    alt="${user.full_name}" 
                                                    width="26" 
                                                    height="26" 
                                                    class="rounded-circle m-1"
                                                 />`
                                              : `
                                                <div 
                                                    class="d-flex justify-content-center align-items-center 
                                                           m-1 bg-dark rounded-circle adaptive-font" 
                                                    style="width: 26px; height: 26px;"
                                                >
                                                  <span class="text-light fw-bold">${user.initials}</span>
                                                </div>
                                              `
                                          }
                                        </div>
                                        <span class="user-name px-1 fw-bold hoverable-text">${user.full_name}</span>
                                    </div>
                                    
                                    ${
                                        user.friendship_status 
                                            ? `<span 
                                                  class="badge rounded-pill text-bg-${user.friendship_status.style}"
                                                  >${user.friendship_status.value}</span>` 
                                            : ""
                                    }
                                  </div>
                                `;

                                searchResultsDropdown.appendChild(listItem);
                            });
                        }

                        searchResultsDropdown.style.display = "contents";
                    });
            }, 500);
        } else {
            friendSearchbar.classList.remove("with-results");
            searchResultsDropdown.style.display = "none";
        }
    });
});