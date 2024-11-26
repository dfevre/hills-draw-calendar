document.addEventListener("DOMContentLoaded", () => {
    const seasonDropdown = document.getElementById("season");
    const divisionDropdown = document.getElementById("division");
    const teamDropdown = document.getElementById("team");
    const result = document.getElementById("result");

    // Declare selectedSeason in a broader scope
    let selectedSeason = null;

    // Fetch seasons.json
    fetch("https://s3.ap-southeast-2.amazonaws.com/fevre.io/data/seasons")
        .then(response => response.json())
        .then(data => {
            // Add a dummy option as the first item
            const dummyOption = document.createElement("option");
            dummyOption.value = "";
            dummyOption.textContent = "Select Season";
            dummyOption.disabled = true;
            dummyOption.selected = true;
            seasonDropdown.appendChild(dummyOption);

            // Populate the dropdown with real data
            if (Array.isArray(data.data)) {
                data.data.forEach(season => {
                    const option = document.createElement("option");
                    option.value = season.season_id;
                    option.textContent = season.season_name;
                    seasonDropdown.appendChild(option);
                });
            } else {
                console.error("Unexpected data format:", data);
            }
        })
        .catch(err => console.error("Failed to load seasons:", err));

    // Update division dropdown on season change
    seasonDropdown.addEventListener("change", () => {
        selectedSeason = seasonDropdown.value; // Update the globally scoped variable
        fetch(`https://s3.ap-southeast-2.amazonaws.com/fevre.io/data/season/${selectedSeason}/divisions`)
            .then(response => response.json())
            .then(data => {
                if (Array.isArray(data.data)) {
                    divisionDropdown.innerHTML = "<option>Select Division</option>";

                    data.data.forEach(division => {
                        const option = document.createElement("option");
                        option.value = division.division_id;
                        option.textContent = division.division_name;
                        divisionDropdown.appendChild(option);
                    });
                } else {
                    console.error("Unexpected data format:", data);
                }
            })
            .catch(err => console.error("Failed to load divisions:", err));
    });

    // Update team dropdown on division change
    divisionDropdown.addEventListener("change", () => {
        const selectedDivision = divisionDropdown.value;
        fetch(`https://s3.ap-southeast-2.amazonaws.com/fevre.io/data/season/${selectedSeason}/division/${selectedDivision}/teams`)
            .then(response => response.json())
            .then(data => {
                teamDropdown.innerHTML = "<option>Select Team</option>";
                if (Array.isArray(data.data)) {
                    data.data.forEach(team => {
                        const option = document.createElement("option");
                        option.value = team.team_id;
                        option.textContent = team.team_name;
                        teamDropdown.appendChild(option);
                    });
                } else {
                    console.error("Unexpected data format:", data);
                }
            })
            .catch(err => console.error("Failed to load teams:", err));
    });

    // Generate URL
    document.getElementById("generate-url").addEventListener("click", () => {
        const season = seasonDropdown.value;
        const division = divisionDropdown.value;
        const teamOption = teamDropdown.options[teamDropdown.selectedIndex]; // Get the selected option
        let teamName = teamOption ? teamOption.textContent : ""; // Get the team name as a string

        if (season && division && teamName) {
            // Replace spaces with '+' and then URL encode the string
            teamName = encodeURIComponent(teamName.replace(/ /g, "+"));

            // Construct the calendar URL
            const url = `https://s3.ap-southeast-2.amazonaws.com/fevre.io/cals/${season}-${division}-${teamName}.ics`;

            // Create a temporary anchor element
            const anchor = document.createElement("a");
            anchor.href = url;
            anchor.download = `${season}-${division}-${teamName}.ics`; // Set the file name for the download
            anchor.style.display = "none"; // Hide the anchor element

            // Append the anchor to the body, trigger the download, and remove it
            document.body.appendChild(anchor);
            anchor.click();
            document.body.removeChild(anchor);
        } else {
            result.textContent = "Please select all options!";
            result.style.color = "red";
        }
    });
});
