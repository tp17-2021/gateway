<script type="ts">
    import Button from "../../../lib/components/buttons/Button.svelte";
    import {goto} from "@roxi/routify";
    import ButtonsContainer from "../../../lib/components/buttons/ButtonsContainer.svelte";
    import {report} from "../../../lib/stores";
    import Input from "../../../lib/components/Input.svelte";
    import KioskBoard from 'kioskboard';
    import {onMount} from "svelte";
    import VirtualInput from "../../../lib/components/VirtualInput.svelte";

    function next() {
        if (president.name === "") {
            alert("Please enter a president name");
            return;
        }
        if (members.length === 0) {
            alert("Please enter at least one member name");
            return;
        }
        $goto("/home/reports/consent");
    }

    function home() {
        $goto("/home");
    }

    let president = $report.president;
    let members = $report.participated_members;
    let newMemberName = "";

    function addMember() {
        let newMemberObject = {
            name: newMemberName,
            agree: false,
        };
        if (newMemberName !== "") {
            members = [...members, newMemberObject];
            newMemberName = "";
        }

        console.log(domNextCandidate)

        setTimeout(() => {
            domNextCandidate.focus();
        }, 50);
    }

    function removeMember(index) {
        members = members.filter((_, i) => i !== index);
    }


    /**
     * Automatically update report store on change
     */
    function updateStore(president, members) {
        $report.president = president
        $report.participated_members = members.sort((a, b) => a.name.localeCompare(b.name));
    }

    $: updateStore(president, members);  // watch for changes


    function handleKeyDown(e) {
        if (e.key === "Enter") {
            addMember();
        }
    }


    onMount(() => {
        // Select the input or the textarea element(s) to run the KioskBoard

        KioskBoard.run('.virtual-keyboard', {

            /*!
            * Required
            * An Array of Objects has to be defined for the custom keys. Hint: Each object creates a row element (HTML) on the keyboard.
            * e.g. [{"key":"value"}, {"key":"value"}] => [{"0":"A","1":"B","2":"C"}, {"0":"D","1":"E","2":"F"}]
            */
            keysArrayOfObjects: [
                {
                    "0": "ď",
                    "1": "ľ",
                    "2": "š",
                    "3": "č",
                    "4": "ť",
                    "5": "ž",
                    "6": "ý",
                    "7": "á",
                    "8": "í",
                    "9": "é",
                    "10": "ó"
                },
                {
                    "0": "Q",
                    "1": "W",
                    "2": "E",
                    "3": "R",
                    "4": "T",
                    "5": "z",
                    "6": "U",
                    "7": "I",
                    "8": "O",
                    "9": "P",
                    "10": "ú",
                    "11": "ä"
                },
                {
                    "0": "A",
                    "1": "S",
                    "2": "D",
                    "3": "F",
                    "4": "G",
                    "5": "H",
                    "6": "J",
                    "7": "K",
                    "8": "L",
                    "9": "ô",
                    "10": "ň"
                },
                {
                    "0": "y",
                    "1": "X",
                    "2": "C",
                    "3": "V",
                    "4": "B",
                    "5": "N",
                    "6": "M",
                    "7": ",",
                    "8": ".",
                    "9": "-"
                }
            ],

            /*!
            * Required only if "keysArrayOfObjects" is "null".
            * The path of the "kioskboard-keys-${langugage}.json" file must be set to the "keysJsonUrl" option. (XMLHttpRequest to get the keys from JSON file.)
            * e.g. '/Content/Plugins/KioskBoard/dist/kioskboard-keys-english.json'
            */
            keysJsonUrl: null,

            /*
            * Optional: An Array of Strings can be set to override the built-in special characters.
            * e.g. ["#", "€", "%", "+", "-", "*"]
            */
            keysSpecialCharsArrayOfStrings: null,

            /*
            * Optional: An Array of Numbers can be set to override the built-in numpad keys. (From 0 to 9, in any order.)
            * e.g. [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
            */
            keysNumpadArrayOfNumbers: null,

            // Optional: (Other Options)

            // Language Code (ISO 639-1) for custom keys (for language support) => e.g. "de" || "en" || "fr" || "hu" || "tr" etc...
            language: 'en',

            // The theme of keyboard => "light" || "dark" || "flat" || "material" || "oldschool"
            theme: 'light',

            // Uppercase or lowercase to start. Uppercased when "true"
            capsLockActive: false,

            /*
            * Allow or prevent real/physical keyboard usage. Prevented when "false"
            * In addition, the "allowMobileKeyboard" option must be "true" as well, if the real/physical keyboard has wanted to be used.
            */
            allowRealKeyboard: true,

            // Allow or prevent mobile keyboard usage. Prevented when "false"
            allowMobileKeyboard: true,

            // CSS animations for opening or closing the keyboard
            cssAnimations: false,

            // CSS animations duration as millisecond
            cssAnimationsDuration: 360,

            // CSS animations style for opening or closing the keyboard => "slide" || "fade"
            cssAnimationsStyle: 'slide',

            // Enable or Disable Spacebar functionality on the keyboard. The Spacebar will be passive when "false"
            keysAllowSpacebar: true,

            // Text of the space key (Spacebar). Without text => " "
            keysSpacebarText: 'Medzera',

            // Font family of the keys
            keysFontFamily: 'sans-serif',

            // Font size of the keys
            keysFontSize: '22px',

            // Font weight of the keys
            keysFontWeight: 'normal',

            // Size of the icon keys
            keysIconSize: '25px',

            // Scrolls the document to the top or bottom(by the placement option) of the input/textarea element. Prevented when "false"
            autoScroll: true,
        });

    });
    let domNextCandidate;


</script>

<style lang="scss">
  .inputContainer {
    display: grid;
    grid-template-columns: 1fr 100px;
    gap: 1rem;
    align-items: center;

    * {
      justify-self: stretch;
    }
  }

</style>

<h1>Úprava zoznamu členov</h1>
<h2>Predseda</h2>
<VirtualInput bind:value={president.name}/>

<h2>Členovia</h2>
{#each members as member, index}
    <div class="inputContainer">
        <div>{member.name}</div>
        <Button on:click={()=>removeMember(index)} type="error" size="small">✖</Button>
    </div>
{/each}

<!--<form on:submit|preventDefault={handleSubmit}>-->
<div class="inputContainer">
    <VirtualInput bind:value={newMemberName} on:keydown={handleKeyDown} bind:domInput={domNextCandidate}/>
    <Button on:click={addMember} type="primary">✓</Button>
</div>
<!--</form> submit={true}-->

<ButtonsContainer>
    <Button on:click={next} type="primary">Ďalej na odsúhlasenie zápisnice</Button>
    <Button on:click={home}>Späť</Button>
</ButtonsContainer>