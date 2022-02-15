<script>
    export let text = "";
    let links = [
        {
            text: "Home",
            href: "/"
        },
        {
            text: "Auth",
            href: "/pin"
        },
        {
            text: "statuses",
        }
    ];
</script>

<style lang="scss">
  @import 'node_modules/@id-sk/frontend/govuk/components/breadcrumbs/_breadcrumbs.scss';
</style>

<div class="govuk-breadcrumbs">
    <ol class="govuk-breadcrumbs__list">
        {#each links as link}
            {#if link?.href}
                <li class="govuk-breadcrumbs__list-item">
                    <a class="govuk-breadcrumbs__link" href="{link.href}">{link.text}</a>
                </li>
            {:else}
                <li class="govuk-breadcrumbs__list-item">
                    {link.text}
                </li>
            {/if}
        {/each}
    </ol>
</div>