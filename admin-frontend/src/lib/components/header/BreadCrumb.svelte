<!--<script>-->

<!--    import {page} from '@roxi/routify';-->
<!--    import {onMount} from "svelte";-->

<!--    let paths = [];-->

<!--    function updatePaths(pathname) {-->
<!--        // // loop url, delimeter /-->
<!--        // paths = pathname.split('/')-->
<!--        // paths = paths.filter(path => {-->
<!--        //         if (path == '')-->
<!--        //             return false-->
<!--        //         else-->
<!--        //             return !["", "admin-frontend"].includes(path);-->
<!--        //     }-->
<!--        // )-->

<!--        console.log(paths, $page.url.pathname);-->
<!--        console.log(paths, $page);-->
<!--    }-->

<!--    onMount(() => {-->


<!--        // updatePaths($page.url.pathname);-->
<!--    });-->

<!--    $: updatePaths($page.url.pathname);-->
<!--</script>-->
<!--<style lang="scss">-->
<!--  @import 'node_modules/@id-sk/frontend/govuk/components/breadcrumbs/_breadcrumbs.scss';-->
<!--</style>-->


<!--<div class="govuk-breadcrumbs">-->
<!--    <ol class="govuk-breadcrumbs__list">-->
<!--        {#each paths as path, index }-->
<!--            &lt;!&ndash; if not last&ndash;&gt;-->
<!--            {#if paths.length !== index  + 1}-->
<!--                <li class="govuk-breadcrumbs__list-item">-->
<!--                    <a class="govuk-breadcrumbs__link" href={paths.slice(0, index + 1).join("/")}>{path}</a>-->
<!--                </li>-->
<!--            {:else}-->
<!--                <li class="govuk-breadcrumbs__list-item">-->
<!--                    {path}-->
<!--                </li>-->
<!--            {/if}-->
<!--        {/each}-->
<!--    </ol>-->
<!--</div>-->