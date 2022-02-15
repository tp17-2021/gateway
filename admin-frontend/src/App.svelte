<script>
  import { Router } from "@roxi/routify";
  import { routes } from "../.routify/routes";

  const config = {
      urlTransform: {
          // set base url based on environment variable
          apply: (url) => `${import.meta.env.VITE_BASE_PATH}${url}`, //external URL
          remove: (url) => url.replace(`${import.meta.env.VITE_BASE_PATH}`, '') //internal URL
      }
  };
</script>

<Router {routes} {config} />