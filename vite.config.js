import { defineConfig } from 'vite';
import reactRefresh from '@vitejs/plugin-react-refresh';
const reactSvgPlugin = require('vite-plugin-react-svg');
// https://vitejs.dev/config/
export default defineConfig({
    build: {
        // generate manifest.json in outDir
        manifest: true,
        rollupOptions: {
            // overwrite default .html entry
            input: {
                url_editor:
                    'templates/admin/annotation/urleditor/all-urls/src/index.jsx',
                new_admin_dash:
                    'templates/admin/new_admin_dash/admin_dash/src/index.jsx',
                sub_manager:
                    'templates/admin/subscriptions/sub_manager/src/index.jsx',
                taxonomy_change_feed:
                    'templates/admin/classification/taxonomyfeed/app/src/index.jsx',
                sku_mapper_editor: 
                    'templates/admin/classification/skumappereditor/sku_mapper/src/index.jsx',
            },
        },
        outDir: 'static/',
    },
    plugins: [
        reactRefresh(),
        reactSvgPlugin({
            // Default behavior when importing `.svg` files, possible options are: 'url' and `component`
            defaultExport: 'component',
        }),
    ],
});
