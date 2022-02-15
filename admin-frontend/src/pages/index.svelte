<script>
    import {metatags, url} from '@roxi/routify'
    
    metatags.title = 'My Routify app'
    metatags.description = 'Description coming soon...'
</script>

<h1>Routify Starter Template</h1>

<p>
    To see an example app that shows off a lot of Routify's features, go to <a href="{$url('/example')}">/example</a>
</p>

<p>
    This template is ready to be used in production! just delete the example app at: src/pages/example
</p>

<a href="{$url('/home')}">Go to home</a>