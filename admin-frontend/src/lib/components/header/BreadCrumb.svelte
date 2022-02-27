<script>
    let paths = []
    import {page, url} from '@roxi/routify'


    function updatePaths(pathname) {
        paths = pathname.split('/')

        paths = paths.filter(path => {
                return !["", "admin-frontend", "gateway", "index"].includes(path);
            }
        )

        console.log(paths, $page);
    }

    $: updatePaths($page.path);
</script>
<style lang="scss">
  @import 'node_modules/@id-sk/frontend/govuk/components/breadcrumbs/_breadcrumbs.scss';
</style>


<div class="govuk-breadcrumbs">
    <ol class="govuk-breadcrumbs__list">
        {#each paths as path, index }
            <!-- if not last-->
            {#if paths.length !== index  + 1}
                <li class="govuk-breadcrumbs__list-item">
                    <a class="govuk-breadcrumbs__link" href={$url("/" + paths.slice(0, index + 1).join("/"))}>{path}</a>
                </li>
            {:else}
                <li class="govuk-breadcrumbs__list-item">
                    {path}
                </li>
            {/if}
        {/each}
    </ol>
</div>