<script>
	import { goto } from "$app/navigation";
	import { api } from "$lib";
	import { onMount } from "svelte";

    let preferences = $state({})
    let word = $state({})
    let showAnswer = $state(false)

    onMount(async() => {   
        load()
    })

    const load = async() => {
        const response = await api('learn/guess/', {
            method: 'GET'
        })

        if (response.ok) {
            const data = await response.json()
            
            Object.assign(preferences, data.preferences)
            Object.assign(word, data.word)
        }

        return response
    }

    const update = async(score) => {
        showAnswer = false

        const data = {
            id: word.id,
            score: score
        }

        const response = await api('learn/score/', {
            method: 'POST',
            body: JSON.stringify(data),
            headers: {
                'Content-Type': 'application/json'
            },
        })

        if (response.ok) {
            load()
        }
    }

</script>

<div class="card bg-base-100 w-96 shadow-sm">
    <div class="card-body">
      <h2 class="card-title">Can you guess the word ?</h2>
      <card-body>
        <p>{preferences.languageA} - { word[preferences.languageA] }</p>
        <label class="swap">
            <input type="checkbox" bind:checked={showAnswer}/>
            <div class="swap-on">{ word[preferences.languageB] }</div>
            <div class="swap-off">click for answer</div>
        </label>      
      </card-body>
      <p>{ word['description'] }</p>
      <div class="card-actions justify-end">
        <button onclick={() => update(1)} class="btn btn-primary">Good</button>
        <button onclick={() => update(-1)} class="btn btn-neutral">Bad</button>
      </div>
    </div>
  </div>