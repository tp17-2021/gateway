<script lang="ts">

    let reports = [
        {
            id: 1,
            title: "Report 1",
            description: "This is the first report",
            date: "2020-01-01",
            status: "Pending"
        },
        {
            id: 2,
            title: "Report 2",
            description: "This is the second report",
            date: "2020-01-02",
            status: "Pending"
        },
        {
            id: 3,
            title: "Report 3",
            description: "This is the third report",
            date: "2020-01-03",
            status: "Pending"
        },
        {
            id: 4,
            title: "Report 4",
            description: "This is the fourth report",
            date: "2020-01-04",
            status: "Pending"
        },
        {
            id: 5,
            title: "Report 5",
            description: "This is the fifth report",
            date: "2020-01-05",
            status: "Pending"
        },
        {
            id: 6,
            title: "Report 6",
            description: "This is the sixth report",
            date: "2020-01-06",
            status: "Pending"
        },
        {
            id: 7,
            title: "Report 7",
            description: "This is the seventh report",
            date: "2020-01-07",
            status: "Pending"
        },
        {
            id: 8,
            title: "Report 8",
            description: "This is the eighth report",
            date: "2020-01-08",
            status: "Pending"
        },
        {
            id: 9,
            title: "Report 9",
            description: "This is the ninth report",
            date: "2020-01-09",
            status: "Pending"
        }
    ];

    reports = reports.map(report => {
        return {...report, "checked": false}
    });

    let selectedReportsIDs = [];
    let selectedAll = false;
    $: {
        selectedReportsIDs = reports.filter(report => report.checked).map(report => report.id);
        console.log(selectedReportsIDs)
        selectedAll = selectedReportsIDs.length === reports.length;
    }

    function selectReport(report) {
        report.checked = !report.checked;
        reports = reports
        console.log(report.checked);
    }

    function selectDeselectAll() {
        selectedAll = !selectedAll;
        reports.forEach(report => report.checked = selectedAll);
    }

</script>

<style lang="scss">
  .reports {
    .report {
      display: flex;
      flex-direction: row;
      align-items: center;
      padding: 1rem;
      gap: 1rem;
      border-bottom: 1px solid #ccc;

      &:hover {
        background-color: #f5f5f5;
      }
    }
  }
</style>

<h1>Zoznam zápisníc</h1>

<div class="report-checkbox">
    <label>
        <input type="checkbox" bind:checked={selectedAll} on:click={selectDeselectAll} />
        Označiť všetky
    </label>

</div>

<div class="reports">
    {#each reports as report}
        <div class="report" on:click={()=>selectReport(report)}>
            <div class="report-checkbox">
                <input type="checkbox" bind:checked={report.checked} />
            </div>
            <div class="report-id">
                <span>{report.id}</span>
            </div>
            <div class="report-button">
                <button>Zobraziť</button>
            </div>
        </div>
    {/each}
</div>